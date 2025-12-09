#!/usr/bin/env python3
"""
Check Vercel deployment logs for catered-by-me project.
"""

import os
import sys
from pathlib import Path

# Add infra to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from infra.providers.vercel_client import VercelClient
    from infra.utils.yaml_loader import load_config, load_provider_configs
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("\nInstalling required packages...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "python-dotenv", "httpx", "PyGithub", "-q"], check=False)
    from infra.providers.vercel_client import VercelClient
    from infra.utils.yaml_loader import load_config, load_provider_configs
    from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Ensure stdout encoding is utf-8
sys.stdout.reconfigure(encoding='utf-8')

def main():
    project_name = "catered-by-me"
    
    print(f"🔍 Checking Vercel deployment for: {project_name}")
    print("=" * 60)
    
    try:
        # Load configs
        config = load_config()
        provider_configs = load_provider_configs()
        vercel_config = provider_configs.get("vercel", {})
        
        projects = vercel_config.get("projects", {})
        if project_name not in projects:
            print(f"ERROR: Project '{project_name}' not found in config")
            print(f"Available projects: {', '.join(projects.keys())}")
            sys.exit(1)
        
        project_config = projects[project_name]
        project_id = project_config.get("project_id") or project_name
        
        # Create client
        vercel_client = VercelClient(vercel_config, env="prod", dry_run=False)
        
        # Get latest deployment
        print(f"\n[1/3] Fetching latest deployment for project: {project_id}")
        deployments = vercel_client._list_deployments(project_id, limit=1)
        
        if not deployments:
            print("WARNING: No deployments found")
            sys.exit(1)
        
        latest = deployments[0]
        deployment_id = latest.get("uid")
        state = latest.get("state")
        ready_state = latest.get("readyState")
        url = latest.get("url", "N/A")
        
        print(f"   Deployment ID: {deployment_id}")
        print(f"   URL: https://{url}")
        print(f"   State: {state}")
        print(f"   Ready State: {ready_state}")
        
        # Get logs
        print(f"\n[2/3] Fetching build logs...")
        logs = vercel_client.get_deployment_logs(deployment_id)
        
        if logs:
            print(f"\nBuild Logs (last 50 lines):")
            print("=" * 60)
            for log_line in logs[-50:]:
                try:
                    print(log_line)
                except UnicodeEncodeError:
                    print(log_line.encode('ascii', 'replace').decode('ascii'))
        else:
            print("WARNING: No logs found")
        
        # Check for errors
        print(f"\n[3/3] Checking for errors...")
        if state == "ERROR" or ready_state == "ERROR":
            print("❌ ERROR: Deployment failed!")
            if logs:
                log_text = "\n".join(logs).lower()
                if "error" in log_text or "failed" in log_text:
                    print("\nError detected in logs (see above)")
            sys.exit(1)
        elif state == "READY" or ready_state == "READY":
            print("✅ SUCCESS: Deployment successful!")
            print(f"\n🌐 Site URL: https://{url}")
        elif state == "BUILDING" or ready_state == "BUILDING":
            print("⏳ IN PROGRESS: Deployment still building...")
        else:
            print(f"⚠️  WARNING: Unknown state: {state}/{ready_state}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

