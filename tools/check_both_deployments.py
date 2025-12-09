#!/usr/bin/env python3
"""Check deployment status for both achillies and catered-by-me."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from infra.providers.vercel_client import VercelClient
from infra.utils.yaml_loader import load_config, load_provider_configs
from dotenv import load_dotenv

load_dotenv()

def check_project(project_name, vercel_client, vercel_config):
    """Check deployment status for a project."""
    print(f"\n{'='*60}")
    print(f"Checking: {project_name}")
    print('='*60)
    
    projects = vercel_config.get("projects", {})
    if project_name not in projects:
        print(f"WARNING: Project '{project_name}' not found in config")
        return None
    
    project_config = projects[project_name]
    project_id = project_config.get("project_id") or project_name
    
    try:
        deployments = vercel_client._list_deployments(project_id, limit=1)
        
        if not deployments:
            print("WARNING: No deployments found")
            return None
        
        latest = deployments[0]
        deployment_id = latest.get("uid")
        state = latest.get("state")
        ready_state = latest.get("readyState")
        url = latest.get("url", "N/A")
        
        print(f"Deployment ID: {deployment_id}")
        print(f"URL: https://{url}")
        print(f"State: {state}")
        print(f"Ready State: {ready_state}")
        
        if state == "ERROR" or ready_state == "ERROR":
            print("STATUS: ERROR - Build failed")
            logs = vercel_client.get_deployment_logs(deployment_id)
            if logs:
                print("\nLast 10 log lines:")
                for log_line in logs[-10:]:
                    try:
                        print(f"  {log_line}")
                    except:
                        pass
        elif state == "READY" or ready_state == "READY":
            print("STATUS: SUCCESS - Deployed!")
        elif state == "BUILDING" or ready_state == "BUILDING":
            print("STATUS: BUILDING - Still in progress")
        else:
            print(f"STATUS: UNKNOWN - {state}/{ready_state}")
        
        return {
            "name": project_name,
            "state": state,
            "ready_state": ready_state,
            "url": url,
            "success": state == "READY" or ready_state == "READY"
        }
    except Exception as e:
        print(f"ERROR checking {project_name}: {e}")
        return None

def main():
    config = load_config()
    provider_configs = load_provider_configs()
    vercel_config = provider_configs.get("vercel", {})
    vercel_client = VercelClient(vercel_config, env="prod", dry_run=False)
    
    print("Vercel Deployment Status Check")
    print("="*60)
    
    results = []
    
    # Check achillies (Corporate Crashout)
    results.append(check_project("achillies", vercel_client, vercel_config))
    
    # Check catered-by-me
    results.append(check_project("catered-by-me", vercel_client, vercel_config))
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    
    for result in results:
        if result:
            status = "SUCCESS" if result["success"] else "FAILED/BUILDING"
            print(f"{result['name']}: {status} - https://{result['url']}")
    
    print("="*60)

if __name__ == "__main__":
    main()

