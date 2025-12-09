#!/usr/bin/env python3
"""
Automated deployment script for Corporate Crashout (achillies).

This script:
1. Verifies/fixes root directory in Vercel
2. Ensures environment variables are set
3. Monitors deployment status
4. Fixes issues automatically
5. Verifies site is live
"""

import os
import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from infra.providers.vercel_client import VercelClient
from infra.providers.vercel_fixer import VercelFixer
from infra.providers.cloudflare_client import CloudflareClient
from infra.utils.yaml_loader import load_provider_configs
from dotenv import load_dotenv
import httpx

load_dotenv()

# Ensure stdout encoding is utf-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PROJECT_NAME = "achillies"
CORRECT_ROOT_DIR = "apps/corporate-crashout"
DOMAIN = "corporatecrashouttrading.com"


def print_step(step: str):
    """Print a step header."""
    print(f"\n{'='*60}")
    print(f"🔧 {step}")
    print(f"{'='*60}")


def print_success(message: str):
    """Print a success message."""
    print(f"✅ {message}")


def print_error(message: str):
    """Print an error message."""
    print(f"❌ {message}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"⚠️  {message}")


def check_site_accessible(url: str) -> tuple[bool, int]:
    """Check if site is accessible and return status code."""
    try:
        response = httpx.get(f"https://{url}", timeout=10, follow_redirects=True)
        return True, response.status_code
    except Exception as e:
        return False, 0


def main():
    print("\n" + "="*60)
    print("🚀 Corporate Crashout Automated Deployment")
    print("="*60)
    
    try:
        # Load configs
        print_step("Loading configuration...")
        provider_configs = load_provider_configs()
        vercel_config = provider_configs.get("vercel", {})
        
        projects = vercel_config.get("projects", {})
        if PROJECT_NAME not in projects:
            print_error(f"Project '{PROJECT_NAME}' not found in vercel.yaml")
            print("Please add it to infra/providers/vercel.yaml")
            sys.exit(1)
        
        project_config = projects[PROJECT_NAME]
        project_id = project_config.get("project_id") or PROJECT_NAME
        
        # Initialize Vercel client
        print_step("Initializing Vercel client...")
        vercel_client = VercelClient(vercel_config, env="prod", dry_run=False)
        
        # Step 1: Verify/Fix Root Directory
        print_step("Step 1: Verifying root directory configuration...")
        project = vercel_client._get_project(project_id)
        
        if not project:
            print_error(f"Project '{project_id}' not found in Vercel")
            print("Please create the project in Vercel dashboard first")
            sys.exit(1)
        
        current_root = project.get("rootDirectory")
        expected_root = project_config.get("root_directory") or CORRECT_ROOT_DIR
        
        print(f"   Current root directory: {current_root or '(not set)'}")
        print(f"   Expected root directory: {expected_root}")
        
        if current_root != expected_root:
            print_warning("Root directory is incorrect - fixing now...")
            success = vercel_client.update_project_settings(
                project_id, root_directory=expected_root
            )
            if success:
                print_success(f"Root directory updated to: {expected_root}")
                # Wait a moment for the change to propagate
                time.sleep(2)
            else:
                print_error("Failed to update root directory")
                print("You may need to update it manually in Vercel dashboard")
        else:
            print_success("Root directory is correct")
        
        # Step 2: Verify Environment Variables
        print_step("Step 2: Verifying environment variables...")
        required_vars = project_config.get("required_env_vars", [])
        missing_vars = []
        
        for var_name in required_vars:
            # Check if var is in config
            env_vars = project_config.get("env_vars", {})
            var_value = None
            
            if var_name in env_vars:
                env_source = env_vars[var_name]
                if isinstance(env_source, str) and env_source.startswith("from_env:"):
                    env_key = env_source.replace("from_env:", "")
                    var_value = os.getenv(env_key)
                else:
                    var_value = str(env_source)
            
            if not var_value:
                missing_vars.append(var_name)
                print_warning(f"Missing: {var_name}")
            else:
                print_success(f"Found: {var_name}")
        
        if missing_vars:
            print_warning(f"Some environment variables are missing: {', '.join(missing_vars)}")
            print("These should be set in Vercel dashboard or .env file")
            print("Continuing anyway - deployment may fail if these are critical...")
        
        # Step 3: Trigger Redeploy if root directory was fixed
        if current_root != expected_root:
            print_step("Step 3: Triggering redeploy with new root directory...")
            deployments = vercel_client._list_deployments(project_id, limit=1)
            if deployments:
                latest = deployments[0]
                deployment_id = latest.get("uid")
                print(f"   Latest deployment: {deployment_id}")
                
                new_deployment = vercel_client.trigger_redeploy(deployment_id)
                if new_deployment:
                    new_id = new_deployment.get("uid") or new_deployment.get("id")
                    print_success(f"Redeploy triggered: {new_id}")
                else:
                    print_warning("Could not trigger redeploy automatically")
                    print("Vercel will auto-deploy on next push, or trigger manually in dashboard")
        
        # Step 4: Monitor Deployment
        print_step("Step 4: Monitoring deployment status...")
        deployments = vercel_client._list_deployments(project_id, limit=1)
        
        if not deployments:
            print_warning("No deployments found")
            print("Waiting for deployment to start...")
            time.sleep(5)
            deployments = vercel_client._list_deployments(project_id, limit=1)
        
        if deployments:
            latest = deployments[0]
            deployment_id = latest.get("uid")
            state = latest.get("state")
            url = latest.get("url")
            
            print(f"   Deployment ID: {deployment_id}")
            print(f"   Current state: {state}")
            print(f"   URL: {url}")
            
            if state in ["BUILDING", "QUEUED", "INITIALIZING"]:
                print("   Waiting for deployment to complete...")
                result = vercel_client.wait_for_deployment(deployment_id, timeout=600, poll_interval=10)
                state = result.get("state", state)
                print(f"   Final state: {state}")
            
            if state == "READY":
                print_success("Deployment is ready!")
                
                # Step 5: Verify Site is Accessible
                print_step("Step 5: Verifying site is accessible...")
                if url:
                    accessible, status_code = check_site_accessible(url)
                    if accessible:
                        if status_code == 200:
                            print_success(f"Site is live! Status: {status_code}")
                            print(f"   URL: https://{url}")
                        elif status_code == 404:
                            print_error("Site returns 404 - root directory may still be incorrect")
                            print("   This might take a few minutes to propagate")
                            print("   Or check Vercel dashboard → Settings → General → Root Directory")
                        else:
                            print_warning(f"Site returned status {status_code}")
                            print(f"   URL: https://{url}")
                    else:
                        print_warning("Could not verify site accessibility")
                else:
                    # Try production domain
                    project_url = project.get("link", {}).get("url")
                    if project_url:
                        accessible, status_code = check_site_accessible(project_url.replace("https://", ""))
                        if accessible and status_code == 200:
                            print_success(f"Site is live! Status: {status_code}")
                            print(f"   URL: https://{project_url}")
                        else:
                            print_warning(f"Production domain returned status {status_code}")
            elif state in ["ERROR", "CANCELED"]:
                print_error(f"Deployment failed with state: {state}")
                
                # Try to auto-fix
                print_step("Attempting to auto-fix issues...")
                fixer = VercelFixer(vercel_client, PROJECT_NAME, project_config, max_retries=3)
                issues = fixer.detect_issues()
                
                if issues:
                    print(f"   Found {len(issues)} issue(s)")
                    for issue in issues:
                        print(f"   - {issue.get('type')}: {issue.get('message', 'No message')}")
                    
                    fix_result = fixer.apply_fixes(issues)
                    if fix_result.success:
                        print_success(f"Applied fixes: {', '.join(fix_result.fixes_applied)}")
                        if fix_result.errors:
                            print_warning(f"Some fixes had errors: {', '.join(fix_result.errors)}")
                    else:
                        print_error(f"Could not apply fixes: {fix_result.message}")
                else:
                    print_warning("No auto-fixable issues detected")
                    print("Check deployment logs in Vercel dashboard")
        
        # Final Summary
        print("\n" + "="*60)
        print("📋 Deployment Summary")
        print("="*60)
        print(f"✅ Root directory: {expected_root}")
        print(f"✅ Project: {project_id}")
        print(f"✅ Latest deployment: {deployment_id if deployments else 'None'}")
        
        if deployments:
            latest = deployments[0]
            state = latest.get("state")
            url = latest.get("url")
            print(f"✅ Status: {state}")
            if url:
                print(f"✅ Preview URL: https://{url}")
        
        project_url = project.get("link", {}).get("url")
        if project_url:
            print(f"✅ Production URL: https://{project_url}")
        
        # Step 6: Update Cloudflare DNS if configured
        print_step("Step 6: Updating Cloudflare DNS...")
        try:
            provider_configs = load_provider_configs()
            cloudflare_config = provider_configs.get("cloudflare", {})
            
            if cloudflare_config and (os.getenv("CLOUDFLARE_API_TOKEN") or os.getenv("CLOUDFLARE_EMAIL")):
                cloudflare = CloudflareClient(cloudflare_config, env="prod", dry_run=False)
                
                # Add domain to Vercel first
                try:
                    domain_result = vercel_client.add_domain(project_id, DOMAIN)
                    print_success(f"Domain added to Vercel: {DOMAIN}")
                except Exception as e:
                    if "already exists" in str(e).lower() or "409" in str(e):
                        print_warning(f"Domain {DOMAIN} already exists in Vercel")
                    else:
                        print_warning(f"Could not add domain to Vercel: {e}")
                
                # Get DNS configuration from Vercel
                dns_config = vercel_client.get_domain_config(DOMAIN)
                if dns_config and dns_config.get("dns_records"):
                    dns_records = dns_config.get("dns_records", [])
                    
                    # Find A record or CNAME for root domain
                    vercel_ip = None
                    vercel_cname = None
                    for record in dns_records:
                        if record.get("type") == "A" and (not record.get("name") or record.get("name") == "@" or record.get("name") == DOMAIN):
                            vercel_ip = record.get("value")
                        elif record.get("type") == "CNAME" and (not record.get("name") or record.get("name") == "@" or record.get("name") == DOMAIN):
                            vercel_cname = record.get("value")
                    
                    if vercel_ip or vercel_cname:
                        print(f"   Vercel DNS: {'IP ' + vercel_ip if vercel_ip else 'CNAME ' + vercel_cname}")
                        print(f"   Updating Cloudflare DNS to point to Vercel...")
                        
                        try:
                            dns_result = cloudflare.update_root_domain_to_vercel(
                                domain=DOMAIN,
                                vercel_ip=vercel_ip,
                                vercel_cname=vercel_cname
                            )
                            if dns_result.get("updated") or dns_result.get("created"):
                                print_success(dns_result.get("message", "DNS updated successfully"))
                                print_warning("DNS propagation may take 5-10 minutes")
                            else:
                                print_warning("DNS update may have failed - check manually")
                        except Exception as e:
                            print_error(f"Failed to update Cloudflare DNS: {e}")
                            print("   You may need to update DNS manually in Cloudflare dashboard")
                    else:
                        print_warning("Could not determine Vercel DNS configuration")
                        print("   Check Vercel dashboard → Settings → Domains for DNS records")
                else:
                    print_warning("Vercel domain configuration not available yet")
                    print("   Domain may need to be added in Vercel dashboard first")
            else:
                print_warning("Cloudflare not configured - skipping DNS update")
                print("   Set CLOUDFLARE_API_TOKEN environment variable to enable DNS automation")
        except Exception as e:
            print_warning(f"Cloudflare DNS update skipped: {e}")
        
        print("\n🎉 Deployment automation complete!")
        print("\nNext steps:")
        print("1. Check Vercel dashboard for deployment status")
        print("2. Verify site is accessible at production URL")
        print("3. If DNS was updated, wait 5-10 minutes for propagation")
        
    except Exception as e:
        print_error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
