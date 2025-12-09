"""Check gallery page status on live site"""

import httpx
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs

print("=" * 70)
print("GALLERY PAGE STATUS CHECK")
print("=" * 70)
print()

# Check Vercel deployment
print("1. Checking Vercel deployment...")
try:
    configs = load_provider_configs()
    vercel_config = configs.get("vercel", {})
    
    if vercel_config:
        client = VercelClient(vercel_config, env="prod", dry_run=False)
        projects = vercel_config.get("projects", {})
        project_config = projects.get("wedding", {})
        project_id = project_config.get("project_id") or "wedding"
        
        deployments = client._list_deployments(project_id, limit=3)
        
        if deployments:
            print(f"   Found {len(deployments)} recent deployment(s):")
            print()
            for i, dep in enumerate(deployments, 1):
                state = dep.get("state")
                url = dep.get("url")
                created = dep.get("createdAt")
                
                from datetime import datetime
                if created:
                    dt = datetime.fromtimestamp(created / 1000)
                    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    time_str = "Unknown"
                
                status_icon = "✅" if state == "READY" else "🔨" if state == "BUILDING" else "❌" if state == "ERROR" else "⏳"
                print(f"   {i}. {status_icon} {state} - {time_str}")
                print(f"      URL: {url}")
                
                if state == "READY":
                    # Test gallery page
                    print()
                    print(f"2. Testing gallery page on {url}...")
                    try:
                        gallery_url = f"{url}/gallery"
                        response = httpx.get(gallery_url, timeout=10, follow_redirects=True)
                        if response.status_code == 200:
                            print(f"   ✅ Gallery page is accessible!")
                            print(f"   URL: {gallery_url}")
                        else:
                            print(f"   ❌ Gallery page returned {response.status_code}")
                    except Exception as e:
                        print(f"   ⚠️  Error testing gallery: {e}")
                
                print()
        else:
            print("   ⚠️  No deployments found")
    else:
        print("   ❌ Vercel config not found")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test live site
print("3. Testing live site (britandkarl.com/gallery)...")
try:
    response = httpx.get("https://britandkarl.com/gallery", timeout=10, follow_redirects=True)
    if response.status_code == 200:
        print("   ✅ Gallery page is LIVE on britandkarl.com!")
    elif response.status_code == 404:
        print("   ❌ Gallery page returns 404 - not deployed yet or route missing")
    else:
        print(f"   ⚠️  Gallery page returned status {response.status_code}")
except Exception as e:
    print(f"   ❌ Error accessing gallery: {e}")

print()
print("=" * 70)
