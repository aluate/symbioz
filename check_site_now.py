"""Quick check if wedding site is live"""

import httpx
import sys
from datetime import datetime

url = "https://britandkarl.com"

print("=" * 70)
print("WEDDING SITE STATUS CHECK")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)
print()
print(f"Checking: {url}")
print()

try:
    response = httpx.get(url, timeout=10, follow_redirects=True)
    status = response.status_code
    
    print(f"HTTP Status Code: {status}")
    print()
    
    if status == 200:
        print("✅ ✅ ✅ SITE IS LIVE! ✅ ✅ ✅")
        print()
        print(f"Response time: {response.elapsed.total_seconds():.2f} seconds")
        print(f"Content length: {len(response.content)} bytes")
    elif 200 <= status < 300:
        print(f"⚠️  Site responded with status {status}")
        print("   (Unexpected but may be working)")
    elif status == 404:
        print("❌ Site returned 404 - Page not found")
    elif status == 500:
        print("❌ Site returned 500 - Server error")
    else:
        print(f"❌ Site returned status {status}")
        print("   Site is NOT accessible")
    
    print()
    print("=" * 70)
    
except httpx.TimeoutException:
    print("❌ ❌ ❌ SITE IS DOWN - TIMEOUT ❌ ❌ ❌")
    print()
    print("The site did not respond within 10 seconds.")
    print("This usually means:")
    print("  - Site is not accessible")
    print("  - DNS is not resolving")
    print("  - Server is not responding")
    print()
    print("=" * 70)
    sys.exit(1)
    
except httpx.RequestError as e:
    print("❌ ❌ ❌ SITE IS DOWN - CONNECTION ERROR ❌ ❌ ❌")
    print()
    print(f"Error: {e}")
    print()
    print("This usually means:")
    print("  - DNS is not configured correctly")
    print("  - Domain is not pointing to Vercel")
    print("  - Site is not deployed")
    print()
    print("=" * 70)
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error checking site: {e}")
    print()
    print("=" * 70)
    sys.exit(1)
