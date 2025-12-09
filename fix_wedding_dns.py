"""Script to help fix wedding site DNS configuration"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "infra"))

from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs

print("=" * 70)
print("WEDDING SITE DNS FIX HELPER")
print("=" * 70)
print()

# Get Vercel domain configuration
try:
    configs = load_provider_configs()
    vercel_config = configs.get("vercel", {})
    
    if vercel_config:
        client = VercelClient(vercel_config, env="prod", dry_run=False)
        projects = vercel_config.get("projects", {})
        project_config = projects.get("wedding", {})
        project_id = project_config.get("project_id") or "wedding"
        
        print("1. Getting Vercel domain configuration...")
        print()
        
        # Get domain config for britandkarl.com
        domain_config = client.get_domain_config("britandkarl.com")
        
        if domain_config:
            print("Domain: britandkarl.com")
            print(f"Status: {domain_config.get('status', 'unknown')}")
            print(f"Misconfigured: {domain_config.get('misconfigured', False)}")
            print()
            
            # Get DNS records needed
            print("2. DNS Records Needed in Cloudflare:")
            print()
            
            # Check if we can get the CNAME target
            nameservers = domain_config.get("nameservers", [])
            if nameservers:
                print("Nameservers:")
                for ns in nameservers:
                    print(f"  - {ns}")
                print()
            
            # Get project domains to see what's configured
            try:
                project_domains = client._get_project_domains(project_id)
                if project_domains:
                    print("3. Current Vercel Domain Configuration:")
                    print()
                    for domain in project_domains.get("domains", []):
                        name = domain.get("name")
                        status = domain.get("verification", {}).get("status", "unknown")
                        print(f"  {name}: {status}")
            except:
                pass
            
        else:
            print("⚠️  Could not get domain configuration")
            print("   Domain may not be added in Vercel yet")
        
        print()
        print("=" * 70)
        print("MANUAL STEPS REQUIRED")
        print("=" * 70)
        print()
        print("1. In Cloudflare, add DNS record for root domain:")
        print("   - Type: CNAME")
        print("   - Name: @")
        print("   - Content: (check Vercel dashboard for correct value)")
        print("   - Proxy: DNS only")
        print()
        print("2. In Vercel, check domain configuration:")
        print("   - Go to: https://vercel.com/aluates-projects/wedding/settings/domains")
        print("   - Click on britandkarl.com")
        print("   - Click 'Learn more' to see what needs fixing")
        print()
        print("3. Wait 10-30 minutes for DNS propagation")
        print()
        print("4. Verify fix:")
        print("   python check_site_now.py")
        print()
        
    else:
        print("⚠️  Vercel config not found")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("=" * 70)
