#!/usr/bin/env python3
"""Get Vercel deployment error logs (simple version without emojis)"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
workspace_root = Path(__file__).parent
env_path = workspace_root / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Add infra to path
sys.path.insert(0, str(workspace_root / "infra"))

from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_provider_configs

def get_error_logs():
    """Get error logs from latest failed deployment"""
    try:
        configs = load_provider_configs()
        client = VercelClient(configs.get("vercel", {}), env="prod", dry_run=False)
        
        # Get project config
        projects = configs.get("vercel", {}).get("projects", {})
        project_config = projects.get("catered-by-me")
        if not project_config:
            print("Project config not found")
            return
        
        project_id = project_config.get("project_id") or "catered-by-me"
        
        # Get latest deployment
        deployments = client._list_deployments(project_id, limit=1)
        if not deployments:
            print("No deployments found")
            return
        
        latest = deployments[0]
        deployment_id = latest.get("uid")
        state = latest.get("state")
        
        print(f"Deployment ID: {deployment_id}")
        print(f"State: {state}")
        print()
        
        if state == "ERROR":
            print("Fetching error logs...")
            print("=" * 60)
            logs = client.get_deployment_logs(deployment_id)
            
            if logs:
                # Show last 150 lines (most relevant)
                for line in logs[-150:]:
                    print(line)
            else:
                print("No logs available")
            
            print("=" * 60)
        else:
            print(f"Deployment state is {state}, not ERROR")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    get_error_logs()

