#!/usr/bin/env python3
"""
Deploy Symbioz/Mellivox - Find service ID and deploy with Otto
If service doesn't exist, we'll note it and you can create it manually
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import httpx
import yaml

# Load .env file
load_dotenv()

api_key = os.getenv("RENDER_API_KEY")
if not api_key:
    print("❌ Error: RENDER_API_KEY not found in .env file")
    sys.exit(1)

print("🚀 Deploying Symbioz/Mellivox with Otto...\n")

# Find Symbioz service
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
        repo = str(service_data.get("repo", "")).lower()
        
        if "symbioz" in name or "mellivox" in name or "symbioz" in repo:
            symbioz_service = service_data
            break
    
    service_id = None
    if symbioz_service:
        service_id = symbioz_service.get("id")
        print(f"✅ Found Render service: {symbioz_service.get('name')} (ID: {service_id})")
    else:
        print("⚠️  No Symbioz Render service found.")
        print("\n💡 You need to create the Render service first:")
        print("   1. Go to https://dashboard.render.com")
        print("   2. Create new Web Service")
        print("   3. Connect repo: aluate/symbioz")
        print("   4. Root directory: apps/symbioz_cli")
        print("   5. Build: pip install -r requirements.txt")
        print("   6. Start: uvicorn api_server:app --host 0.0.0.0 --port $PORT")
        print("   7. Copy the service ID (srv-xxxxx) from the URL")
        print("\n   Then update infra/providers/render.yaml with the service ID")
        print("   Or run: python find_symbioz_service_id.py")
        print()
        
        # Check if config has placeholder
        render_yaml_path = Path("infra/providers/render.yaml")
        with open(render_yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
        
        current_id = config.get("services", {}).get("symbioz-api", {}).get("render_service_id", "")
        if current_id and current_id != "srv-REPLACE_WITH_ACTUAL_SERVICE_ID":
            print(f"📝 Config has service ID: {current_id}")
            print("   Using that for deployment...")
            service_id = current_id
        else:
            print("❌ Cannot proceed without Render service ID")
            print("   Please create the service and update the config, then run again.")
            sys.exit(1)
    
    # Update config if we found a service
    if symbioz_service:
        render_yaml_path = Path("infra/providers/render.yaml")
        with open(render_yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
        
        services_config = config.get("services", {})
        if "symbioz-api" in services_config:
            old_id = services_config["symbioz-api"].get("render_service_id", "")
            if old_id != service_id:
                services_config["symbioz-api"]["render_service_id"] = service_id
                with open(render_yaml_path, 'w', encoding='utf-8') as f:
                    yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
                print(f"✅ Updated config: {old_id} → {service_id}")
    
    # Deploy with Otto
    print("\n🚀 Starting deployment with Otto...")
    print("=" * 60)
    
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
        if result.data:
            iterations = result.data.get("iterations", 0)
            print(f"   Completed in {iterations} iteration(s)")
            if result.data.get("vercel", {}).get("url"):
                print(f"   🌐 URL: {result.data['vercel']['url']}")
    else:
        print(f"❌ FAILED: {result.message}")
        if result.data:
            if result.data.get("render"):
                render = result.data["render"]
                if not render.get("success"):
                    print(f"   Render: {render.get('message', 'Unknown error')}")
            if result.data.get("vercel"):
                vercel = result.data["vercel"]
                if not vercel.get("success"):
                    print(f"   Vercel: {vercel.get('message', 'Unknown error')}")
    print("=" * 60)
    
    sys.exit(0 if result.success else 1)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

