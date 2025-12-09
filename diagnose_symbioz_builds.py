#!/usr/bin/env python3
"""Diagnose Symbioz build errors in detail."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import httpx
import yaml

load_dotenv()

print("Diagnosing Symbioz Build Errors...")
print("=" * 60)

api_key = os.getenv("RENDER_API_KEY")
vercel_token = os.getenv("VERCEL_TOKEN")

# Check Render Backend
print("\n[Render Backend API]")
print("-" * 60)

try:
    render_yaml_path = Path("infra/providers/render.yaml")
    with open(render_yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}
    
    services = config.get("services", {})
    symbioz_config = services.get("symbioz-api", {})
    service_id = symbioz_config.get("render_service_id", "")
    
    if service_id and api_key:
        # Get service info
        url = f"https://api.render.com/v1/services/{service_id}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }
        
        response = httpx.get(url, headers=headers, timeout=30.0)
        if response.status_code == 200:
            service_data = response.json().get("service", response.json())
            
            # Get deployments
            deploy_url = f"https://api.render.com/v1/services/{service_id}/deploys"
            deploy_response = httpx.get(deploy_url, headers=headers, timeout=30.0)
            if deploy_response.status_code == 200:
                deploys = deploy_response.json()
                if deploys and len(deploys) > 0:
                    latest = deploys[0].get("deploy", deploys[0])
                    deploy_status = latest.get("status", "unknown")
                    deploy_id = latest.get("id", "")
                    
                    print(f"Service: {service_data.get('name', 'N/A')}")
                    print(f"Status: {deploy_status}")
                    print(f"Deploy ID: {deploy_id}")
                    
                    # Get build logs
                    if deploy_id and deploy_status == "build_failed":
                        log_url = f"https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}/logs"
                        log_response = httpx.get(log_url, headers=headers, timeout=30.0)
                        if log_response.status_code == 200:
                            logs_data = log_response.json()
                            logs = logs_data.get("logs", [])
                            print("\nBuild Logs (last 100 lines):")
                            print("-" * 60)
                            for log_entry in logs[-100:]:
                                if isinstance(log_entry, dict):
                                    print(log_entry.get("message", ""))
                                else:
                                    print(log_entry)
                        else:
                            print(f"Could not get logs: HTTP {log_response.status_code}")
                            
except Exception as e:
    print(f"Error checking Render: {e}")

# Check Vercel Frontend
print("\n[Vercel Frontend]")
print("-" * 60)

try:
    vercel_yaml_path = Path("infra/providers/vercel.yaml")
    with open(vercel_yaml_path, 'r', encoding='utf-8') as f:
        vercel_config = yaml.safe_load(f) or {}
    
    projects = vercel_config.get("projects", {})
    symbioz_project = projects.get("symbioz", {})
    project_id = symbioz_project.get("project_id", "symbioz")
    
    if vercel_token:
        headers = {
            "Authorization": f"Bearer {vercel_token}",
            "Accept": "application/json",
        }
        
        # Get project
        project_url = f"https://api.vercel.com/v9/projects/{project_id}"
        project_response = httpx.get(project_url, headers=headers, timeout=30.0)
        
        if project_response.status_code == 200:
            project_data = project_response.json()
            print(f"Project: {project_data.get('name', project_id)}")
            
            # Get deployments
            deploy_url = "https://api.vercel.com/v13/deployments"
            params = {"projectId": project_id, "limit": 1}
            deploy_response = httpx.get(deploy_url, headers=headers, params=params, timeout=30.0)
            
            if deploy_response.status_code == 200:
                deployments = deploy_response.json().get("deployments", [])
                if deployments:
                    latest = deployments[0]
                    state = latest.get("state", "unknown")
                    deploy_id = latest.get("uid", "")
                    url_deploy = latest.get("url", "")
                    
                    print(f"Status: {state}")
                    print(f"Deploy ID: {deploy_id}")
                    if url_deploy:
                        print(f"URL: https://{url_deploy}")
                    
                    # Get build logs if failed
                    if state == "ERROR" and deploy_id:
                        # Get events/logs
                        events_url = f"https://api.vercel.com/v2/deployments/{deploy_id}/events"
                        events_response = httpx.get(events_url, headers=headers, timeout=30.0)
                        if events_response.status_code == 200:
                            events = events_response.json()
                            print("\nBuild Events (errors):")
                            print("-" * 60)
                            for event in events.get("events", [])[-50:]:
                                if event.get("type") == "command" and event.get("payload", {}).get("exitCode") != 0:
                                    print(event.get("payload", {}).get("text", ""))
                                elif event.get("type") == "stderr":
                                    print(event.get("payload", {}).get("text", ""))
                else:
                    print("No deployments found")
            elif deploy_response.status_code == 400:
                print(f"HTTP 400 error - possible issue with project ID or permissions")
                print(f"Response: {deploy_response.text[:200]}")
        elif project_response.status_code == 404:
            print(f"Project '{project_id}' not found")
        else:
            print(f"Error: HTTP {project_response.status_code}")
            print(f"Response: {project_response.text[:200]}")
            
except Exception as e:
    print(f"Error checking Vercel: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Diagnosis complete")

