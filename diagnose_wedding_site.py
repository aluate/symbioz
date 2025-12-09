"""Comprehensive wedding site diagnosis"""

import sys
import json
import httpx
from pathlib import Path
from datetime import datetime

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

from infra.utils.health_check import check_health
from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs

WEDDING_SITE_URL = "https://britandkarl.com"
WEDDING_PROJECT = "wedding"
OTTO_API_URL = "http://localhost:8001"

results = {
    "timestamp": datetime.now().isoformat(),
    "site_url": WEDDING_SITE_URL,
    "checks": {}
}

print("=" * 70)
print("WEDDING SITE DIAGNOSIS")
print("=" * 70)
print()

# 1. Check HTTP directly
print("1. Checking HTTP response...")
try:
    http_result = check_health(WEDDING_SITE_URL, timeout=10, retries=2)
    results["checks"]["http"] = http_result
    
    if http_result["status"] == "ok":
        print(f"   ✅ Site is LIVE - Status {http_result['status_code']}, {http_result['response_time_ms']}ms")
    elif http_result["status"] == "warn":
        print(f"   ⚠️  Site responded with status {http_result['status_code']}")
    else:
        print(f"   ❌ Site is NOT accessible")
        print(f"   Error: {http_result.get('error', 'Unknown')}")
except Exception as e:
    print(f"   ❌ Error checking HTTP: {e}")
    results["checks"]["http"] = {"status": "error", "error": str(e)}

print()

# 2. Check Vercel deployment
print("2. Checking Vercel deployment...")
try:
    configs = load_provider_configs()
    vercel_config = configs.get("vercel", {})
    
    if vercel_config:
        client = VercelClient(vercel_config, env="prod", dry_run=False)
        projects = vercel_config.get("projects", {})
        project_config = projects.get(WEDDING_PROJECT, {})
        project_id = project_config.get("project_id") or WEDDING_PROJECT
        
        deployments = client._list_deployments(project_id, limit=3)
        
        if deployments:
            latest = deployments[0]
            state = latest.get("state")
            url = latest.get("url")
            created = latest.get("createdAt")
            
            print(f"   Latest Deployment State: {state}")
            print(f"   Deployment URL: {url}")
            if created:
                from datetime import datetime
                dt = datetime.fromtimestamp(created / 1000)
                print(f"   Created: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
            
            results["checks"]["vercel"] = {
                "status": "found",
                "deployment_state": state,
                "deployment_url": url,
                "created_at": created
            }
            
            if state == "READY":
                print("   ✅ Deployment is READY")
            elif state == "ERROR":
                print("   ❌ Deployment has ERROR")
            elif state == "BUILDING":
                print("   ⏳ Deployment is BUILDING")
            else:
                print(f"   ⚠️  Deployment state: {state}")
        else:
            print("   ⚠️  No deployments found")
            results["checks"]["vercel"] = {"status": "no_deployments"}
    else:
        print("   ⚠️  Vercel config not found")
        results["checks"]["vercel"] = {"status": "no_config"}
except Exception as e:
    print(f"   ❌ Error checking Vercel: {e}")
    results["checks"]["vercel"] = {"status": "error", "error": str(e)}

print()

# 3. Check Otto API
print("3. Checking Otto API...")
try:
    with httpx.Client(timeout=5.0) as client:
        health = client.get(f"{OTTO_API_URL}/health")
        if health.status_code == 200:
            print("   ✅ Otto API is running")
            
            # Try to use Otto to check
            print("   Sending task to Otto...")
            task_response = client.post(
                f"{OTTO_API_URL}/task",
                json={
                    "type": "deployment.check_status",
                    "payload": {
                        "platform": "vercel",
                        "project": "wedding"
                    },
                    "source": "wedding_site_check"
                },
                timeout=30.0
            )
            
            if task_response.status_code == 200:
                otto_result = task_response.json()
                print(f"   ✅ Otto Response: {otto_result.get('message', 'No message')[:100]}")
                results["checks"]["otto"] = {
                    "status": "success",
                    "response": otto_result
                }
            else:
                print(f"   ⚠️  Otto returned status {task_response.status_code}")
                results["checks"]["otto"] = {
                    "status": "error",
                    "status_code": task_response.status_code
                }
        else:
            print(f"   ⚠️  Otto API returned {health.status_code}")
            results["checks"]["otto"] = {"status": "unavailable"}
except httpx.ConnectError:
    print("   ⚠️  Otto API is not running")
    results["checks"]["otto"] = {"status": "not_running"}
except Exception as e:
    print(f"   ⚠️  Error with Otto: {e}")
    results["checks"]["otto"] = {"status": "error", "error": str(e)}

print()

# Summary
print("=" * 70)
print("SUMMARY")
print("=" * 70)

http_status = results["checks"].get("http", {}).get("status")
vercel_state = results["checks"].get("vercel", {}).get("deployment_state")

if http_status == "ok":
    print("✅ Site is LIVE and accessible")
elif http_status == "error":
    print("❌ Site is NOT accessible")
    print()
    print("DIAGNOSIS:")
    if vercel_state == "ERROR":
        print("  - Vercel deployment has ERROR")
        print("  - Check Vercel dashboard for build logs")
    elif vercel_state == "READY":
        print("  - Vercel deployment is READY but site not accessible")
        print("  - Likely DNS or domain configuration issue")
    else:
        print("  - Unknown issue - check all systems")
    
    print()
    print("NEXT STEPS:")
    print("  1. Check Vercel dashboard: https://vercel.com/aluates-projects/wedding")
    print("  2. Check DNS in Cloudflare")
    print("  3. Verify domain is still active")
    print("  4. Check SSL certificate status")
else:
    print(f"⚠️  Site status: {http_status}")

# Save results
output_file = Path(__file__).parent / "wedding_diagnosis.json"
with open(output_file, "w") as f:
    json.dump(results, f, indent=2)
print()
print(f"Full results saved to: {output_file}")
print("=" * 70)
