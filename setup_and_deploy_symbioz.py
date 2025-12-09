#!/usr/bin/env python3
"""
Setup Symbioz Render service and deploy everything with Otto
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import httpx
import yaml

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("RENDER_API_KEY")
if not api_key:
    print("❌ Error: RENDER_API_KEY not found in .env file")
    sys.exit(1)

print("🚀 Setting up Symbioz/Mellivox deployment...\n")

# Step 1: Check if service exists
print("Step 1: Checking for existing Render service...")
url = "https://api.render.com/v1/services"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
}

try:
    response = httpx.get(url, headers=headers, timeout=30.0)
    response.raise_for_status()
    services = response.json()
    
    symbioz_service = None
    for service in services:
        service_data = service.get("service", {})
        name = service_data.get("name", "").lower()
        repo = service_data.get("repo", "").lower()
        
        if "symbioz" in name or "mellivox" in name or "symbioz" in repo or "mellivox" in repo:
            symbioz_service = service_data
            break
    
    if symbioz_service:
        service_id = symbioz_service.get("id")
        print(f"✅ Found existing service: {symbioz_service.get('name')} (ID: {service_id})")
    else:
        print("⚠️  No existing service found. Creating new Render service...")
        # Create service
        create_url = "https://api.render.com/v1/services"
        payload = {
            "type": "web_service",
            "name": "symbioz-api",
            "repo": "https://github.com/aluate/symbioz",
            "branch": "main",
            "rootDir": "apps/symbioz_cli",
            "buildCommand": "pip install -r requirements.txt",
            "startCommand": "uvicorn api_server:app --host 0.0.0.0 --port $PORT",
            "envVars": [
                {"key": "PYTHON_VERSION", "value": "3.11.11"}
            ]
        }
        
        create_response = httpx.post(create_url, headers=headers, json=payload, timeout=60.0)
        if create_response.status_code == 201:
            service_data = create_response.json().get("service", {})
            service_id = service_data.get("id")
            print(f"✅ Created new service: {service_data.get('name')} (ID: {service_id})")
        else:
            print(f"❌ Failed to create service: {create_response.status_code} - {create_response.text}")
            print("\n💡 You may need to create the service manually via Render dashboard.")
            print("   Then run this script again to update the config and deploy.")
            sys.exit(1)
    
    # Step 2: Update config
    print("\nStep 2: Updating config file...")
    render_yaml_path = Path("infra/providers/render.yaml")
    with open(render_yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}
    
    services_config = config.get("services", {})
    if "symbioz-api" not in services_config:
        print("❌ symbioz-api not found in config")
        sys.exit(1)
    
    old_id = services_config["symbioz-api"].get("render_service_id", "")
    services_config["symbioz-api"]["render_service_id"] = service_id
    
    with open(render_yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"✅ Updated {render_yaml_path}")
    if old_id != service_id:
        print(f"   Changed: {old_id} → {service_id}")
    
    # Step 3: Deploy with Otto
    print("\nStep 3: Deploying with Otto...")
    print("=" * 60)
    
    # Import and run Otto deployment
    sys.path.insert(0, str(Path(__file__).parent / "apps" / "otto"))
    
    from otto.config import load_config
    from otto.core.models import Task, TaskStatus
    from otto.core.skill_base import SkillContext
    from otto.core.runner import run_tasks
    from otto.core.logging_utils import get_logger
    from otto.skills import get_all_skills
    import uuid
    
    logger = get_logger(__name__)
    config = load_config()
    context = SkillContext(config=config, logger=logger)
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
    
    print(f"📋 Task: {task.type}")
    print(f"   Project: {task.payload['project_name']}")
    print()
    print("⏳ Running deployment automation...")
    print()
    
    results = run_tasks([task], skills, context)
    result = results[0]
    
    print("=" * 60)
    if result.success:
        print(f"✅ SUCCESS: {result.message}")
        if result.data and result.data.get("vercel", {}).get("url"):
            print(f"   🌐 URL: {result.data['vercel']['url']}")
    else:
        print(f"❌ FAILED: {result.message}")
    print("=" * 60)
    
    sys.exit(0 if result.success else 1)
    
except httpx.HTTPStatusError as e:
    print(f"❌ Error: HTTP {e.response.status_code} - {e.response.text}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

