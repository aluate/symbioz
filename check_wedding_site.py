"""Check wedding site status - britandkarl.com"""

import sys
from pathlib import Path
import httpx
import json
from datetime import datetime

# Add infra to path
sys.path.insert(0, str(Path(__file__).parent / "infra"))

from infra.utils.health_check import check_health

WEDDING_SITE_URL = "https://britandkarl.com"
OTTO_API_URL = "http://localhost:8001"

def check_site_directly():
    """Check the wedding site directly"""
    print(f"🔍 Checking wedding site: {WEDDING_SITE_URL}")
    print("-" * 60)
    
    result = check_health(WEDDING_SITE_URL, timeout=10, retries=2)
    
    if result["status"] == "ok":
        print(f"✅ Site is LIVE!")
        print(f"   Status Code: {result['status_code']}")
        print(f"   Response Time: {result['response_time_ms']}ms")
        return True
    elif result["status"] == "warn":
        print(f"⚠️  Site responded but with unexpected status")
        print(f"   Status Code: {result['status_code']}")
        print(f"   Response Time: {result['response_time_ms']}ms")
        return True
    else:
        print(f"❌ Site is NOT accessible")
        if result.get("error"):
            print(f"   Error: {result['error']}")
        if result.get("status_code"):
            print(f"   Status Code: {result['status_code']}")
        return False

def check_via_otto():
    """Check site status via Otto API"""
    print(f"\n🤖 Checking via Otto API...")
    print("-" * 60)
    
    try:
        # First check if Otto API is running
        with httpx.Client(timeout=5.0) as client:
            health_response = client.get(f"{OTTO_API_URL}/health")
            if health_response.status_code != 200:
                print("⚠️  Otto API is not responding")
                return None
            
            # Try to check deployment status via Otto
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
                result = task_response.json()
                print(f"✅ Otto Response: {result.get('message', 'No message')}")
                if result.get("result"):
                    print(f"   Data: {json.dumps(result['result'], indent=2)}")
                return result.get("status") == "success"
            else:
                print(f"⚠️  Otto API returned status {task_response.status_code}")
                print(f"   Response: {task_response.text[:200]}")
                return None
                
    except httpx.ConnectError:
        print("⚠️  Otto API is not running (connection refused)")
        print("   Start Otto with: python -m apps.otto.otto.api")
        return None
    except Exception as e:
        print(f"⚠️  Error checking via Otto: {str(e)}")
        return None

def main():
    print("=" * 60)
    print("Wedding Site Status Check")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check site directly
    site_ok = check_site_directly()
    
    # Try Otto if available
    otto_result = check_via_otto()
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if site_ok:
        print("✅ Wedding site (britandkarl.com) is LIVE and accessible")
    else:
        print("❌ Wedding site (britandkarl.com) is NOT accessible")
        print("\nPossible issues:")
        print("  - DNS not configured correctly")
        print("  - Vercel deployment failed")
        print("  - Domain expired or not pointing to Vercel")
        print("\nNext steps:")
        print("  1. Check Vercel dashboard: https://vercel.com/aluates-projects/wedding")
        print("  2. Check DNS configuration in Cloudflare")
        print("  3. Verify domain is still active")
    
    if otto_result is not None:
        if otto_result:
            print("✅ Otto deployment check: All systems operational")
        else:
            print("⚠️  Otto deployment check: Issues detected")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
