"""Check wedding site status and report results"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

import httpx
from infra.utils.health_check import check_health
from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs

WEDDING_SITE_URL = "https://britandkarl.com"
WEDDING_PROJECT = "wedding"
OTTO_API_URL = "http://localhost:8001"

def check_site_http():
    """Check if site responds to HTTP requests"""
    print("1. Checking HTTP response...")
    result = check_health(WEDDING_SITE_URL, timeout=10, retries=2)
    
    if result["status"] == "ok":
        return {
            "status": "live",
            "status_code": result["status_code"],
            "response_time_ms": result["response_time_ms"],
            "message": "Site is accessible"
        }
    else:
        return {
            "status": "down",
            "error": result.get("error", "Unknown error"),
            "status_code": result.get("status_code"),
            "message": "Site is not accessible"
        }

def check_vercel_deployment():
    """Check Vercel deployment status"""
    print("2. Checking Vercel deployment...")
    
    try:
        configs = load_provider_configs()
        vercel_config = configs.get("vercel", {})
        
        if not vercel_config:
            return {"status": "error", "message": "Vercel config not found"}
        
        client = VercelClient(vercel_config, env="prod", dry_run=False)
        
        # Get project config
        projects = vercel_config.get("projects", {})
        project_config = projects.get(WEDDING_PROJECT, {})
        project_id = project_config.get("project_id") or WEDDING_PROJECT
        
        # Get latest deployment
        deployments = client._list_deployments(project_id, limit=1)
        
        if deployments:
            latest = deployments[0]
            state = latest.get("state")
            url = latest.get("url")
            
            return {
                "status": "found",
                "deployment_state": state,
                "deployment_url": url,
                "created_at": latest.get("createdAt"),
                "message": f"Latest deployment: {state}"
            }
        else:
            return {
                "status": "no_deployments",
                "message": "No deployments found"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Error checking Vercel: {str(e)}"
        }

def check_otto_api():
    """Check if Otto API is available"""
    print("3. Checking Otto API...")
    
    try:
        with httpx.Client(timeout=5.0) as client:
            health = client.get(f"{OTTO_API_URL}/health")
            if health.status_code == 200:
                return {"status": "available", "message": "Otto API is running"}
            else:
                return {"status": "unavailable", "message": f"Otto API returned {health.status_code}"}
    except httpx.ConnectError:
        return {"status": "not_running", "message": "Otto API is not running"}
    except Exception as e:
        return {"status": "error", "error": str(e), "message": f"Error: {str(e)}"}

def main():
    print("=" * 70)
    print("Wedding Site Status Check - britandkarl.com")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "site_url": WEDDING_SITE_URL,
        "checks": {}
    }
    
    # Check HTTP
    http_result = check_site_http()
    results["checks"]["http"] = http_result
    print(f"   {http_result['message']}")
    if http_result.get("status_code"):
        print(f"   Status Code: {http_result['status_code']}")
    if http_result.get("response_time_ms"):
        print(f"   Response Time: {http_result['response_time_ms']}ms")
    print()
    
    # Check Vercel
    vercel_result = check_vercel_deployment()
    results["checks"]["vercel"] = vercel_result
    print(f"   {vercel_result['message']}")
    if vercel_result.get("deployment_state"):
        print(f"   Deployment State: {vercel_result['deployment_state']}")
    if vercel_result.get("deployment_url"):
        print(f"   Deployment URL: {vercel_result['deployment_url']}")
    print()
    
    # Check Otto
    otto_result = check_otto_api()
    results["checks"]["otto"] = otto_result
    print(f"   {otto_result['message']}")
    print()
    
    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    
    http_live = http_result.get("status") == "live"
    vercel_ok = vercel_result.get("deployment_state") == "READY"
    
    if http_live:
        print("✅ Wedding site (britandkarl.com) is LIVE and accessible")
    else:
        print("❌ Wedding site (britandkarl.com) is NOT accessible")
        print()
        print("Possible issues:")
        print("  - DNS not configured correctly")
        print("  - Vercel deployment failed or not ready")
        print("  - Domain expired or not pointing to Vercel")
        print("  - SSL certificate issue")
        print()
        print("Next steps:")
        print("  1. Check Vercel dashboard: https://vercel.com/aluates-projects/wedding")
        print("  2. Check DNS configuration in Cloudflare")
        print("  3. Verify domain is still active")
        print("  4. Check if deployment is in ERROR state")
    
    if vercel_result.get("deployment_state"):
        if vercel_ok:
            print("✅ Vercel deployment is READY")
        elif vercel_result.get("deployment_state") == "ERROR":
            print("❌ Vercel deployment has ERROR - check logs")
        elif vercel_result.get("deployment_state") == "BUILDING":
            print("⏳ Vercel deployment is BUILDING - wait for completion")
        else:
            print(f"⚠️  Vercel deployment state: {vercel_result.get('deployment_state')}")
    
    # Save results
    output_file = Path(__file__).parent / "wedding_site_status.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print()
    print(f"Full results saved to: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
