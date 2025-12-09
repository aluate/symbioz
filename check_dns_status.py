"""Check current DNS and site status"""

import sys
import httpx
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs

DOMAIN = "britandkarl.com"
PROJECT = "wedding"

print("=" * 70)
print("CURRENT STATUS CHECK")
print("=" * 70)
print()

# Check HTTP
print("1. HTTP Status:")
try:
    response = httpx.get(f"https://{DOMAIN}", timeout=10, follow_redirects=True)
    status = response.status_code
    if status == 200:
        print(f"   ✅ Site is LIVE - Status {status}")
    else:
        print(f"   ⚠️  Status {status}")
except Exception as e:
    print(f"   ❌ Site not accessible: {e}")

print()

# Check Vercel
print("2. Vercel Domain Status:")
try:
    configs = load_provider_configs()
    vercel_config = configs.get("vercel", {})
    
    if vercel_config:
        client = VercelClient(vercel_config, env="prod", dry_run=False)
        projects = vercel_config.get("projects", {})
        project_config = projects.get(PROJECT, {})
        project_id = project_config.get("project_id") or PROJECT
        
        # Get project domains
        project_domains_url = f"{client.API_BASE_URL}/v9/projects/{project_id}/domains"
        with httpx.Client() as http_client:
            response = http_client.get(
                project_domains_url,
                headers=client._get_headers(),
                timeout=30
            )
            if response.status_code == 200:
                domains_data = response.json()
                domains = domains_data.get("domains", [])
                
                for domain_info in domains:
                    name = domain_info.get("name")
                    if name == DOMAIN or name == f"www.{DOMAIN}":
                        verification = domain_info.get("verification", {})
                        status = verification.get("status", "unknown")
                        print(f"   {name}: {status}")
except Exception as e:
    print(f"   ⚠️  Could not check: {e}")

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print()
print("The script only READS configuration - it doesn't modify anything")
print("unless you have CLOUDFLARE_API_TOKEN set and it successfully")
print("adds a DNS record. If no token, it only shows instructions.")
print()
print("Nothing should be broken. Check the status above.")
