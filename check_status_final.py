"""Final status check - writes to file"""

import sys
import httpx
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs

url = "https://britandkarl.com"
project = "wedding"

output = []
output.append("=" * 70)
output.append("WEDDING SITE STATUS CHECK")
output.append(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
output.append("=" * 70)
output.append("")

# Check HTTP
output.append("1. Checking HTTP response...")
try:
    response = httpx.get(url, timeout=10, follow_redirects=True)
    status = response.status_code
    if status == 200:
        output.append(f"   ✅ SITE IS LIVE! Status: {status}")
        site_live = True
    else:
        output.append(f"   ❌ Site returned status {status}")
        site_live = False
except Exception as e:
    output.append(f"   ❌ Site is NOT accessible")
    output.append(f"   Error: {str(e)}")
    site_live = False

output.append("")

# Check Vercel
output.append("2. Checking Vercel deployment...")
try:
    configs = load_provider_configs()
    vercel_config = configs.get("vercel", {})
    
    if vercel_config:
        client = VercelClient(vercel_config, env="prod", dry_run=False)
        projects = vercel_config.get("projects", {})
        project_config = projects.get(project, {})
        project_id = project_config.get("project_id") or project
        
        deployments = client._list_deployments(project_id, limit=1)
        
        if deployments:
            latest = deployments[0]
            state = latest.get("state")
            deploy_url = latest.get("url")
            
            output.append(f"   Deployment State: {state}")
            output.append(f"   Deployment URL: {deploy_url}")
            
            if state == "READY":
                output.append("   ✅ Deployment is READY")
                if not site_live:
                    output.append("   ⚠️  But site not accessible - likely DNS issue")
            elif state == "ERROR":
                output.append("   ❌ Deployment has ERROR")
            elif state == "BUILDING":
                output.append("   ⏳ Deployment is BUILDING")
            else:
                output.append(f"   ⚠️  Unknown state: {state}")
        else:
            output.append("   ⚠️  No deployments found")
    else:
        output.append("   ⚠️  Vercel config not found")
except Exception as e:
    output.append(f"   ❌ Error: {str(e)}")

output.append("")
output.append("=" * 70)

# Write to file
result_text = "\n".join(output)
print(result_text)

with open("site_status_check.txt", "w") as f:
    f.write(result_text)
