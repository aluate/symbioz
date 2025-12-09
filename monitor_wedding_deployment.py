"""Monitor wedding site deployment until successful"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs

PROJECT = "wedding"
CHECK_INTERVAL = 10  # Check every 10 seconds
MAX_CHECKS = 60  # Check for up to 10 minutes (60 * 10s)

def check_deployment():
    """Check latest deployment status"""
    try:
        configs = load_provider_configs()
        vercel_config = configs.get("vercel", {})
        
        if not vercel_config:
            print("❌ Vercel config not found")
            return None
        
        client = VercelClient(vercel_config, env="prod", dry_run=False)
        projects = vercel_config.get("projects", {})
        project_config = projects.get(PROJECT, {})
        project_id = project_config.get("project_id") or PROJECT
        
        deployments = client._list_deployments(project_id, limit=1)
        
        if deployments:
            latest = deployments[0]
            return {
                "state": latest.get("state"),
                "url": latest.get("url"),
                "created_at": latest.get("createdAt"),
                "uid": latest.get("uid")
            }
        return None
    except Exception as e:
        print(f"❌ Error checking deployment: {e}")
        return None

def main():
    print("=" * 70)
    print("WEDDING SITE DEPLOYMENT MONITOR")
    print("=" * 70)
    print()
    print(f"Monitoring project: {PROJECT}")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print(f"Max checks: {MAX_CHECKS} ({MAX_CHECKS * CHECK_INTERVAL // 60} minutes)")
    print()
    print("Waiting for deployment to start...")
    print()
    
    check_count = 0
    last_state = None
    
    while check_count < MAX_CHECKS:
        check_count += 1
        deployment = check_deployment()
        
        if deployment:
            state = deployment["state"]
            url = deployment.get("url", "N/A")
            
            # Only print if state changed
            if state != last_state:
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                if state == "READY":
                    print(f"[{timestamp}] ✅ ✅ ✅ DEPLOYMENT SUCCESSFUL! ✅ ✅ ✅")
                    print(f"   URL: {url}")
                    print()
                    print("=" * 70)
                    print("SUCCESS! Site is live!")
                    print("=" * 70)
                    return True
                elif state == "ERROR":
                    print(f"[{timestamp}] ❌ Deployment failed")
                    print(f"   URL: {url}")
                    print()
                    print("Checking deployment logs...")
                    try:
                        configs = load_provider_configs()
                        vercel_config = configs.get("vercel", {})
                        client = VercelClient(vercel_config, env="prod", dry_run=False)
                        logs = client.get_deployment_logs(deployment["uid"])
                        if logs:
                            print("   Recent log entries:")
                            for log_entry in logs[-5:]:
                                print(f"      {log_entry}")
                    except:
                        pass
                    print()
                    print("=" * 70)
                    print("DEPLOYMENT FAILED")
                    print("=" * 70)
                    print("Check Vercel dashboard for details:")
                    print(f"https://vercel.com/aluates-projects/{PROJECT}")
                    return False
                elif state == "BUILDING":
                    print(f"[{timestamp}] 🔨 Building...")
                elif state == "QUEUED":
                    print(f"[{timestamp}] ⏳ Queued...")
                else:
                    print(f"[{timestamp}] ⚠️  State: {state}")
                
                last_state = state
        else:
            if check_count == 1:
                print("   ⏳ Waiting for deployment to appear...")
        
        time.sleep(CHECK_INTERVAL)
    
    print()
    print("=" * 70)
    print("TIMEOUT - Stopped monitoring")
    print("=" * 70)
    print(f"Checked {check_count} times over {check_count * CHECK_INTERVAL // 60} minutes")
    print("Deployment may still be in progress.")
    print("Check manually: https://vercel.com/aluates-projects/wedding")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
