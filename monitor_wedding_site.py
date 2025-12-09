"""Monitor wedding site and alert when it goes down"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

import httpx
from infra.utils.health_check import check_health
from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs

WEDDING_SITE_URL = "https://britandkarl.com"
WEDDING_PROJECT = "wedding"
CHECK_INTERVAL = 300  # 5 minutes
LOG_FILE = Path(__file__).parent / "wedding_site_monitor.log"
STATUS_FILE = Path(__file__).parent / "wedding_site_status.json"

def check_site() -> Dict[str, Any]:
    """Check site status"""
    result = {
        "timestamp": datetime.now().isoformat(),
        "url": WEDDING_SITE_URL
    }
    
    # HTTP check
    http_result = check_health(WEDDING_SITE_URL, timeout=10, retries=2)
    result["http"] = http_result
    result["is_live"] = http_result["status"] == "ok"
    
    # Vercel check
    try:
        configs = load_provider_configs()
        vercel_config = configs.get("vercel", {})
        if vercel_config:
            client = VercelClient(vercel_config, env="prod", dry_run=False)
            projects = vercel_config.get("projects", {})
            project_config = projects.get(WEDDING_PROJECT, {})
            project_id = project_config.get("project_id") or WEDDING_PROJECT
            
            deployments = client._list_deployments(project_id, limit=1)
            if deployments:
                latest = deployments[0]
                result["vercel"] = {
                    "state": latest.get("state"),
                    "url": latest.get("url"),
                    "created_at": latest.get("createdAt")
                }
    except Exception as e:
        result["vercel"] = {"error": str(e)}
    
    return result

def log_status(result: Dict[str, Any]):
    """Log status to file"""
    status = "✅ LIVE" if result["is_live"] else "❌ DOWN"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"[{timestamp}] {status} - HTTP {result['http'].get('status_code', 'N/A')}"
    if result.get("vercel", {}).get("state"):
        log_entry += f" - Vercel: {result['vercel']['state']}"
    
    print(log_entry)
    
    # Append to log file
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")
    
    # Save current status
    with open(STATUS_FILE, "w") as f:
        json.dump(result, f, indent=2)

def monitor_once():
    """Run one check"""
    result = check_site()
    log_status(result)
    return result

def monitor_continuous():
    """Monitor continuously"""
    print("=" * 70)
    print("Wedding Site Monitor")
    print(f"Monitoring: {WEDDING_SITE_URL}")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print("Press Ctrl+C to stop")
    print("=" * 70)
    print()
    
    try:
        while True:
            result = monitor_once()
            
            if not result["is_live"]:
                print("⚠️  ALERT: Site is down!")
                print(f"   Error: {result['http'].get('error', 'Unknown')}")
            
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Monitor wedding site")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--interval", type=int, default=300, help="Check interval in seconds")
    
    args = parser.parse_args()
    
    if args.interval:
        CHECK_INTERVAL = args.interval
    
    if args.once:
        monitor_once()
    else:
        monitor_continuous()
