"""Auto-monitor wedding deployment and loop until successful"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

from infra.providers.vercel_client import VercelClient
from infra.providers.vercel_fixer import VercelFixer
from infra.utils.yaml_loader import load_provider_configs

PROJECT = "wedding"
CHECK_INTERVAL = 15  # Check every 15 seconds
MAX_ATTEMPTS = 40  # Check for up to 10 minutes

def check_and_fix():
    """Check deployment and attempt fixes if needed"""
    try:
        configs = load_provider_configs()
        vercel_config = configs.get("vercel", {})
        
        if not vercel_config:
            print("❌ Vercel config not found")
            return None, None
        
        client = VercelClient(vercel_config, env="prod", dry_run=False)
        projects = vercel_config.get("projects", {})
        project_config = projects.get(PROJECT, {})
        project_id = project_config.get("project_id") or PROJECT
        
        deployments = client._list_deployments(project_id, limit=1)
        
        if not deployments:
            return None, None
        
        latest = deployments[0]
        state = latest.get("state")
        url = latest.get("url")
        deployment_id = latest.get("uid")
        
        return {
            "state": state,
            "url": url,
            "uid": deployment_id,
            "created_at": latest.get("createdAt")
        }, (client, project_config)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

def main():
    print("=" * 70)
    print("WEDDING SITE - AUTO MONITOR & FIX")
    print("=" * 70)
    print()
    print(f"Project: {PROJECT}")
    print(f"Monitoring deployment until successful...")
    print()
    
    attempt = 0
    last_state = None
    
    while attempt < MAX_ATTEMPTS:
        attempt += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        deployment, client_info = check_and_fix()
        
        if not deployment:
            if attempt == 1:
                print(f"[{timestamp}] ⏳ Waiting for deployment to appear...")
            time.sleep(CHECK_INTERVAL)
            continue
        
        state = deployment["state"]
        url = deployment.get("url", "N/A")
        
        # Only print on state change
        if state != last_state:
            if state == "READY":
                print(f"[{timestamp}] ✅ ✅ ✅ DEPLOYMENT SUCCESSFUL! ✅ ✅ ✅")
                print(f"   URL: {url}")
                print()
                print("=" * 70)
                print("🎉 SUCCESS! Site is live with photos!")
                print("=" * 70)
                print()
                print("Your photo gallery is now live at:")
                print(f"   {url}/gallery")
                return True
                
            elif state == "ERROR":
                print(f"[{timestamp}] ❌ Deployment failed")
                print(f"   URL: {url}")
                print()
                print("   Attempting to fix...")
                
                # Try to use fixer
                if client_info:
                    client, project_config = client_info
                    try:
                        fixer = VercelFixer(client, PROJECT, project_config, max_retries=1)
                        issues = fixer.detect_issues()
                        
                        if issues:
                            print(f"   Found {len(issues)} issue(s)")
                            fix_result = fixer.apply_fixes(issues)
                            
                            if fix_result.fixes_applied:
                                print(f"   ✅ Applied fixes: {', '.join(fix_result.fixes_applied)}")
                                print("   🔄 Triggering redeployment...")
                                new_deployment_id = fixer.trigger_redeploy()
                                if new_deployment_id:
                                    print(f"   ✅ New deployment triggered: {new_deployment_id}")
                                    last_state = None  # Reset to watch new deployment
                            else:
                                print("   ⚠️  Could not auto-fix")
                                if fix_result.errors:
                                    for error in fix_result.errors:
                                        print(f"      - {error}")
                                
                                # Get logs
                                try:
                                    logs = client.get_deployment_logs(deployment["uid"])
                                    if logs:
                                        print("   Recent errors:")
                                        for log_entry in logs[-3:]:
                                            if "error" in log_entry.lower() or "fail" in log_entry.lower():
                                                print(f"      {log_entry}")
                                except:
                                    pass
                        else:
                            print("   ⚠️  No issues detected (may need manual review)")
                    except Exception as e:
                        print(f"   ⚠️  Fixer error: {e}")
                
                print()
                print("   Check Vercel dashboard:")
                print(f"   https://vercel.com/aluates-projects/{PROJECT}")
                
            elif state == "BUILDING":
                print(f"[{timestamp}] 🔨 Building...")
            elif state == "QUEUED":
                print(f"[{timestamp}] ⏳ Queued...")
            else:
                print(f"[{timestamp}] ⚠️  State: {state}")
            
            last_state = state
        
        time.sleep(CHECK_INTERVAL)
    
    print()
    print("=" * 70)
    print("Monitoring timeout")
    print("=" * 70)
    print(f"Checked {attempt} times over {attempt * CHECK_INTERVAL // 60} minutes")
    print("Deployment may still be in progress.")
    print()
    print("Check manually:")
    print(f"https://vercel.com/aluates-projects/{PROJECT}")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
