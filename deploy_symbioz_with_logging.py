#!/usr/bin/env python3
"""
Deploy Symbioz/Mellivox with full logging
"""

import sys
import uuid
import time
from pathlib import Path
from datetime import datetime

# Add apps/otto to path
sys.path.insert(0, str(Path(__file__).parent / "apps" / "otto"))

from otto.config import load_config
from otto.core.models import Task, TaskStatus
from otto.core.skill_base import SkillContext
from otto.core.runner import run_tasks
from otto.core.logging_utils import get_logger
from otto.skills import get_all_skills

logger = get_logger(__name__)

def log(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)

def main():
    """Run deployment automation for Symbioz/Mellivox"""
    log("🚀 Starting Symbioz/Mellivox deployment with Otto...")
    log("")
    
    # Load config
    try:
        config = load_config()
        context = SkillContext(config=config, logger=logger)
        skills = get_all_skills()
        log(f"✅ Loaded {len(skills)} skills")
    except Exception as e:
        log(f"❌ Error loading config: {e}")
        sys.exit(1)
    
    # Create deployment task
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
    
    log(f"📋 Task: {task.type}")
    log(f"   Project: {task.payload['project_name']}")
    log(f"   Max iterations: {task.payload['max_iterations']}")
    log("")
    log("⏳ Running deployment automation...")
    log("   (This may take 10-15 minutes)")
    log("")
    
    # Run the task
    try:
        results = run_tasks([task], skills, context)
        result = results[0]
    except Exception as e:
        log(f"❌ Error running deployment: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Print results
    log("=" * 60)
    if result.success:
        log(f"✅ SUCCESS: {result.message}")
        log("")
        if result.data:
            iterations = result.data.get("iterations", 0)
            log(f"   Completed in {iterations} iteration(s)")
            log("")
            
            # Print iteration results
            results_list = result.data.get("results", [])
            if results_list:
                log("   Iteration Summary:")
                for res in results_list:
                    log(f"   - {res}")
                log("")
            
            # Print deployment details
            if result.data.get("render"):
                render = result.data["render"]
                log(f"   Render: {render.get('status', 'unknown')}")
            if result.data.get("vercel"):
                vercel = result.data["vercel"]
                log(f"   Vercel: {vercel.get('status', 'unknown')}")
                if vercel.get("url"):
                    log(f"   🌐 URL: {vercel['url']}")
                    log("")
                    log(f"   🎉 Site is LIVE at: {vercel['url']}")
    else:
        log(f"❌ FAILED: {result.message}")
        log("")
        if result.data:
            iterations = result.data.get("iterations", 0)
            log(f"   Attempted {iterations} iteration(s)")
            log("")
            
            # Print what went wrong
            if result.data.get("render"):
                render = result.data["render"]
                if not render.get("success"):
                    log(f"   Render Error: {render.get('message', 'Unknown error')}")
            if result.data.get("vercel"):
                vercel = result.data["vercel"]
                if not vercel.get("success"):
                    log(f"   Vercel Error: {vercel.get('message', 'Unknown error')}")
                    if vercel.get("errors"):
                        log("   Errors detected:")
                        for error in vercel["errors"]:
                            log(f"     - {error.get('type', 'unknown')}: {error.get('variable', '')}")
    
    log("=" * 60)
    
    sys.exit(0 if result.success else 1)

if __name__ == "__main__":
    main()

