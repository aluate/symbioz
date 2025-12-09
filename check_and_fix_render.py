#!/usr/bin/env python3
"""
Check Render deployment status and let Otto fix it
"""

import os, sys, httpx, yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

print("🔍 Checking Render Deployment Status...")
print("=" * 60)
print()

api_key = os.getenv("RENDER_API_KEY")
if not api_key:
    print("❌ RENDER_API_KEY not found")
    sys.exit(1)

# Load config
config = yaml.safe_load(open("infra/providers/render.yaml"))
service_id = config["services"]["symbioz-api"]["render_service_id"]

print(f"Service ID: {service_id}")
print()

# Get latest deployment
url = f"https://api.render.com/v1/services/{service_id}/deploys"
headers = {"Authorization": f"Bearer {api_key}"}
r = httpx.get(url, headers=headers, params={"limit": 1}, timeout=15)

if r.status_code == 200:
    deps = r.json()
    if deps:
        dep = deps[0].get("deploy", deps[0])
        status = dep.get("status", "unknown")
        deploy_id = dep.get("id", "")
        
        print(f"Status: {status}")
        print(f"Deploy ID: {deploy_id}")
        print()
        
        if status in ["build_failed", "update_failed"]:
            print("❌ Deployment failed!")
            print()
            print("Getting error logs...")
            
            # Get logs
            log_url = f"https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}/logs"
            log_r = httpx.get(log_url, headers=headers, params={"lines": 100}, timeout=15)
            
            if log_r.status_code == 200:
                logs = log_r.text if isinstance(log_r.text, str) else str(log_r.json())
                print("Recent error logs:")
                print("-" * 60)
                print(logs[-1000:] if len(logs) > 1000 else logs)
                print("-" * 60)
            else:
                error_msg = dep.get("message", dep.get("error", "Unknown error"))
                print(f"Error message: {error_msg}")
            
            print()
            print("🚀 Letting Otto fix this...")
            print()
            
            # Now run Otto's deployment automation
            sys.path.insert(0, str(Path(__file__).parent / "apps" / "otto"))
            
            from otto.config import load_config
            from otto.core.models import Task, TaskStatus
            from otto.core.skill_base import SkillContext
            from otto.core.runner import run_tasks
            from otto.core.logging_utils import get_logger
            from otto.skills import get_all_skills
            import uuid
            
            logger = get_logger(__name__)
            otto_config = load_config()
            context = SkillContext(config=otto_config, logger=logger)
            skills = get_all_skills()
            
            task = Task(
                id=str(uuid.uuid4()),
                type="deployment.deploy_and_fix",
                payload={
                    "project_path": ".",
                    "project_name": "symbioz",
                    "max_iterations": 5
                },
                source="cli",
                status=TaskStatus.PENDING
            )
            
            print("Otto is analyzing and fixing...")
            print()
            
            results = run_tasks([task], skills, context)
            result = results[0]
            
            print("=" * 60)
            if result.success:
                print(f"✅ SUCCESS: {result.message}")
                if result.data and result.data.get("vercel", {}).get("url"):
                    print(f"🌐 Site is LIVE at: {result.data['vercel']['url']}")
            else:
                print(f"❌ FAILED: {result.message}")
                if result.data:
                    if result.data.get("render"):
                        print(f"   Render: {result.data['render'].get('message', 'Unknown')}")
                    if result.data.get("vercel"):
                        print(f"   Vercel: {result.data['vercel'].get('message', 'Unknown')}")
            print("=" * 60)
        elif status == "live":
            print("✅ Deployment is LIVE!")
            service_url = f"https://symbioz-api.onrender.com"
            print(f"🌐 URL: {service_url}")
        else:
            print(f"⏳ Status: {status} (still deploying...)")
    else:
        print("⚠️  No deployments found")
else:
    print(f"❌ Error: HTTP {r.status_code}")

