#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Get Vercel deployment error logs with proper encoding"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

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
        
        projects = configs.get("vercel", {}).get("projects", {})
        project_config = projects.get("catered-by-me")
        if not project_config:
            print("Project config not found")
            return
        
        project_id = project_config.get("project_id") or "catered-by-me"
        deployments = client._list_deployments(project_id, limit=1)
        
        if not deployments:
            print("No deployments found")
            return
        
        latest = deployments[0]
        deployment_id = latest.get("uid")
        state = latest.get("state")
        commit = latest.get("meta", {}).get("githubCommitSha", "unknown")[:8]
        
        print(f"Deployment: {deployment_id}")
        print(f"State: {state}")
        print(f"Commit: {commit}")
        print()
        
        if state == "ERROR":
            print("Fetching build logs...")
            print("=" * 70)
            logs = client.get_deployment_logs(deployment_id)
            
            if logs:
                # Find the error section
                error_start = -1
                for i, line in enumerate(logs):
                    if "Error:" in line or "error" in line.lower() or "failed" in line.lower():
                        error_start = max(0, i - 10)  # Show 10 lines before error
                        break
                
                if error_start >= 0:
                    print("\n".join(logs[error_start:]))
                else:
                    # Show last 100 lines
                    print("\n".join(logs[-100:]))
            else:
                print("No logs available")
            
            print("=" * 70)
        else:
            print(f"Deployment state: {state}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    get_error_logs()

