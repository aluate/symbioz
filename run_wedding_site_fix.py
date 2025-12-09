"""Run complete wedding site fix automatically"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

import httpx
from infra.utils.health_check import check_health
from infra.providers.vercel_client import VercelClient
from infra.providers.vercel_fixer import VercelFixer
from infra.utils.yaml_loader import load_provider_configs

WEDDING_SITE_URL = "https://britandkarl.com"
WEDDING_PROJECT = "wedding"

def run_command(cmd, description):
    """Run a command and capture output"""
    print(f"\n{'='*70}")
    print(f"{description}")
    print(f"{'='*70}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout + result.stderr
        print(output)
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        print(f"⚠️  Command timed out")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, str(e)

def main():
    """Run complete fix process"""
    print("=" * 70)
    print("AUTOMATED WEDDING SITE FIX")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "site_url": WEDDING_SITE_URL,
        "project": WEDDING_PROJECT,
        "steps": []
    }
    
    # Step 1: Check HTTP
    print("\n1. Checking HTTP response...")
    http_result = check_health(WEDDING_SITE_URL, timeout=10, retries=2)
    results["steps"].append({
        "step": "http_check",
        "status": http_result["status"],
        "status_code": http_result.get("status_code"),
        "error": http_result.get("error")
    })
    
    if http_result["status"] == "ok":
        print(f"   ✅ Site is LIVE - Status {http_result['status_code']}")
        print("\n" + "=" * 70)
        print("✅ SITE IS LIVE - NO ACTION NEEDED")
        print("=" * 70)
        
        # Save results
        with open("wedding_site_fix_results.json", "w") as f:
            json.dump(results, f, indent=2)
        return
    
    print(f"   ❌ Site is NOT accessible")
    print(f"   Error: {http_result.get('error', 'Unknown')}")
    
    # Step 2: Check Vercel deployment
    print("\n2. Checking Vercel deployment...")
    try:
        configs = load_provider_configs()
        vercel_config = configs.get("vercel", {})
        
        if not vercel_config:
            print("   ❌ Vercel config not found")
            results["steps"].append({
                "step": "vercel_check",
                "status": "error",
                "error": "Vercel config not found"
            })
        else:
            client = VercelClient(vercel_config, env="prod", dry_run=False)
            projects = vercel_config.get("projects", {})
            project_config = projects.get(WEDDING_PROJECT, {})
            project_id = project_config.get("project_id") or WEDDING_PROJECT
            
            deployments = client._list_deployments(project_id, limit=1)
            
            if deployments:
                latest = deployments[0]
                state = latest.get("state")
                url = latest.get("url")
                deployment_id = latest.get("uid")
                
                print(f"   Latest Deployment State: {state}")
                print(f"   Deployment URL: {url}")
                
                results["steps"].append({
                    "step": "vercel_check",
                    "status": "found",
                    "deployment_state": state,
                    "deployment_url": url,
                    "deployment_id": deployment_id
                })
                
                if state == "ERROR":
                    print("   ❌ Deployment has ERROR - attempting to fix...")
                    
                    # Step 3: Use Vercel Fixer
                    print("\n3. Running Vercel auto-fixer...")
                    try:
                        fixer = VercelFixer(client, WEDDING_PROJECT, project_config, max_retries=3)
                        
                        # Detect issues
                        issues = fixer.detect_issues()
                        print(f"   Found {len(issues)} issue(s)")
                        
                        if issues:
                            for issue in issues:
                                print(f"   - {issue.get('type')}: {issue.get('message', 'No message')}")
                        
                        # Apply fixes
                        if issues:
                            fix_result = fixer.apply_fixes(issues)
                            print(f"   Fix Result: {fix_result.message}")
                            
                            if fix_result.fixes_applied:
                                print(f"   ✅ Applied {len(fix_result.fixes_applied)} fix(es):")
                                for fix in fix_result.fixes_applied:
                                    print(f"      - {fix}")
                                
                                # Trigger redeploy
                                print("\n4. Triggering redeployment...")
                                new_deployment_id = fixer.trigger_redeploy()
                                if new_deployment_id:
                                    print(f"   ✅ Redeployment triggered: {new_deployment_id}")
                                    print("   ⏳ Waiting for deployment to complete...")
                                    
                                    deployment_result = fixer.wait_for_deployment(new_deployment_id, timeout=600)
                                    final_state = deployment_result.get("state")
                                    
                                    print(f"   Final state: {final_state}")
                                    
                                    if final_state == "READY":
                                        print("   ✅ Deployment completed successfully!")
                                    else:
                                        print(f"   ⚠️  Deployment state: {final_state}")
                                    
                                    results["steps"].append({
                                        "step": "redeploy",
                                        "status": "completed",
                                        "deployment_id": new_deployment_id,
                                        "final_state": final_state
                                    })
                                else:
                                    print("   ⚠️  Could not trigger redeployment")
                                    results["steps"].append({
                                        "step": "redeploy",
                                        "status": "failed",
                                        "error": "Could not trigger redeployment"
                                    })
                            else:
                                print("   ⚠️  No automatic fixes could be applied")
                                if fix_result.errors:
                                    print("   Errors:")
                                    for error in fix_result.errors:
                                        print(f"      - {error}")
                                
                                results["steps"].append({
                                    "step": "fix_attempt",
                                    "status": "no_fixes",
                                    "errors": fix_result.errors
                                })
                                
                                # Get logs for manual review
                                print("\n5. Fetching deployment logs for manual review...")
                                logs = client.get_deployment_logs(deployment_id)
                                if logs:
                                    print("   Recent log entries:")
                                    for log in logs[-10:]:
                                        print(f"      {log}")
                                    results["steps"].append({
                                        "step": "logs",
                                        "status": "fetched",
                                        "log_count": len(logs)
                                    })
                        else:
                            print("   ✅ No issues detected")
                            results["steps"].append({
                                "step": "fix_attempt",
                                "status": "no_issues"
                            })
                            
                    except Exception as e:
                        print(f"   ❌ Error running fixer: {e}")
                        results["steps"].append({
                            "step": "fix_attempt",
                            "status": "error",
                            "error": str(e)
                        })
                
                elif state == "BUILDING":
                    print("   ⏳ Deployment is BUILDING - wait for completion")
                    results["steps"].append({
                        "step": "vercel_check",
                        "status": "building"
                    })
                
                elif state == "READY":
                    print("   ✅ Deployment is READY but site not accessible")
                    print("   ⚠️  Likely DNS issue")
                    results["steps"].append({
                        "step": "vercel_check",
                        "status": "ready_but_down",
                        "likely_issue": "dns"
                    })
                    
                    # Check domain
                    print("\n3. Checking domain configuration...")
                    success, output = run_command(
                        f'cd apps\\wedding && python check_domain_status.py',
                        "Domain Configuration Check"
                    )
                    results["steps"].append({
                        "step": "domain_check",
                        "status": "completed",
                        "success": success
                    })
            else:
                print("   ⚠️  No deployments found")
                results["steps"].append({
                    "step": "vercel_check",
                    "status": "no_deployments"
                })
                
    except Exception as e:
        print(f"   ❌ Error checking Vercel: {e}")
        results["steps"].append({
            "step": "vercel_check",
            "status": "error",
            "error": str(e)
        })
    
    # Step 4: Verify fix
    print("\n" + "=" * 70)
    print("FINAL VERIFICATION")
    print("=" * 70)
    
    print("\nChecking site again...")
    final_check = check_health(WEDDING_SITE_URL, timeout=10, retries=2)
    
    if final_check["status"] == "ok":
        print(f"   ✅ Site is now LIVE - Status {final_check['status_code']}")
        results["final_status"] = "live"
    else:
        print(f"   ❌ Site is still not accessible")
        print(f"   Error: {final_check.get('error', 'Unknown')}")
        results["final_status"] = "down"
        
        print("\n" + "=" * 70)
        print("MANUAL ACTION REQUIRED")
        print("=" * 70)
        print("\nThe automated fix could not resolve the issue.")
        print("Please check:")
        print("  1. Vercel dashboard: https://vercel.com/aluates-projects/wedding")
        print("  2. DNS configuration in Cloudflare")
        print("  3. Domain registration status")
        print("  4. Deployment logs for build errors")
    
    # Save results
    output_file = Path(__file__).parent / "wedding_site_fix_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
