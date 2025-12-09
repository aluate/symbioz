"""Automated fix script for wedding site issues"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

import httpx
from infra.utils.health_check import check_health
from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs

WEDDING_SITE_URL = "https://britandkarl.com"
WEDDING_PROJECT = "wedding"

def check_and_fix():
    """Check site and attempt to fix issues"""
    print("=" * 70)
    print("AUTOMATED WEDDING SITE FIX")
    print("=" * 70)
    print()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "site_url": WEDDING_SITE_URL,
        "actions_taken": [],
        "issues_found": [],
        "fixes_applied": []
    }
    
    # Step 1: Check HTTP
    print("Step 1: Checking HTTP response...")
    http_result = check_health(WEDDING_SITE_URL, timeout=10, retries=2)
    
    if http_result["status"] == "ok":
        print(f"   ✅ Site is LIVE - Status {http_result['status_code']}")
        results["status"] = "live"
        return results
    else:
        print(f"   ❌ Site is NOT accessible")
        print(f"   Error: {http_result.get('error', 'Unknown')}")
        results["status"] = "down"
        results["issues_found"].append({
            "type": "http",
            "error": http_result.get("error"),
            "status_code": http_result.get("status_code")
        })
    
    print()
    
    # Step 2: Check Vercel deployment
    print("Step 2: Checking Vercel deployment...")
    try:
        configs = load_provider_configs()
        vercel_config = configs.get("vercel", {})
        
        if not vercel_config:
            print("   ⚠️  Vercel config not found")
            results["issues_found"].append({"type": "config", "error": "Vercel config missing"})
            return results
        
        client = VercelClient(vercel_config, env="prod", dry_run=False)
        projects = vercel_config.get("projects", {})
        project_config = projects.get(WEDDING_PROJECT, {})
        project_id = project_config.get("project_id") or WEDDING_PROJECT
        
        deployments = client._list_deployments(project_id, limit=3)
        
        if not deployments:
            print("   ❌ No deployments found")
            results["issues_found"].append({"type": "deployment", "error": "No deployments"})
            print()
            print("   💡 Fix: Push code to GitHub to trigger deployment")
            results["fixes_applied"].append({
                "action": "suggestion",
                "message": "Push code to GitHub to trigger new deployment"
            })
            return results
        
        latest = deployments[0]
        state = latest.get("state")
        url = latest.get("url")
        
        print(f"   Latest Deployment State: {state}")
        print(f"   Deployment URL: {url}")
        
        if state == "ERROR":
            print("   ❌ Deployment has ERROR")
            results["issues_found"].append({
                "type": "deployment_error",
                "state": state,
                "deployment_url": url
            })
            
            # Try to get logs
            print("   Fetching deployment logs...")
            try:
                logs = client.get_deployment_logs(latest.get("uid"))
                if logs:
                    print("   Recent log entries:")
                    for log in logs[-5:]:
                        print(f"      {log}")
                    results["deployment_logs"] = logs[-10:]
            except Exception as e:
                print(f"   ⚠️  Could not fetch logs: {e}")
            
            print()
            print("   💡 Fix: Check Vercel dashboard for full error details")
            print(f"   Dashboard: https://vercel.com/aluates-projects/{WEDDING_PROJECT}")
            results["fixes_applied"].append({
                "action": "manual_review",
                "message": "Check Vercel dashboard for build errors",
                "url": f"https://vercel.com/aluates-projects/{WEDDING_PROJECT}"
            })
            
        elif state == "BUILDING":
            print("   ⏳ Deployment is BUILDING - wait for completion")
            results["issues_found"].append({
                "type": "deployment_building",
                "state": state
            })
            results["fixes_applied"].append({
                "action": "wait",
                "message": "Deployment in progress, wait for completion"
            })
            
        elif state == "READY":
            print("   ✅ Deployment is READY")
            print("   ⚠️  But site is not accessible - likely DNS issue")
            results["issues_found"].append({
                "type": "dns",
                "message": "Deployment ready but site not accessible"
            })
            
            print()
            print("   💡 Fix: Check DNS configuration")
            print("   1. Check Cloudflare DNS records")
            print("   2. Verify domain points to Vercel")
            print("   3. Check SSL/TLS settings")
            print("   4. Run: cd apps\\wedding && python check_domain_status.py")
            results["fixes_applied"].append({
                "action": "check_dns",
                "message": "Check DNS configuration in Cloudflare",
                "command": "cd apps\\wedding && python check_domain_status.py"
            })
        else:
            print(f"   ⚠️  Unknown deployment state: {state}")
            results["issues_found"].append({
                "type": "unknown_state",
                "state": state
            })
            
    except Exception as e:
        print(f"   ❌ Error checking Vercel: {e}")
        results["issues_found"].append({
            "type": "vercel_error",
            "error": str(e)
        })
    
    print()
    
    # Step 3: Summary and recommendations
    print("=" * 70)
    print("SUMMARY & RECOMMENDATIONS")
    print("=" * 70)
    print()
    
    if results["status"] == "live":
        print("✅ Site is LIVE - no action needed")
    else:
        print("❌ Site is DOWN - issues found:")
        for issue in results["issues_found"]:
            print(f"   - {issue.get('type', 'unknown')}: {issue.get('error', issue.get('message', 'Unknown'))}")
        
        print()
        print("Recommended fixes:")
        for fix in results["fixes_applied"]:
            print(f"   • {fix.get('message')}")
            if fix.get("command"):
                print(f"     Run: {fix['command']}")
            if fix.get("url"):
                print(f"     URL: {fix['url']}")
    
    # Save results
    output_file = Path(__file__).parent / "wedding_site_fix_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print()
    print(f"Full results saved to: {output_file}")
    print("=" * 70)
    
    return results

if __name__ == "__main__":
    check_and_fix()
