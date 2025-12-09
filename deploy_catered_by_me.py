#!/usr/bin/env python3
"""
Quick script to ask Otto to deploy catered by me and fix any errors
"""

import sys
import uuid
from pathlib import Path

# Add apps/otto to path
sys.path.insert(0, str(Path(__file__).parent / "apps" / "otto"))

from otto.config import load_config
from otto.core.models import Task, TaskStatus
from otto.core.skill_base import SkillContext
from otto.core.runner import run_tasks
from otto.core.logging_utils import get_logger
from otto.skills import get_all_skills

logger = get_logger(__name__)


def main():
    """Run deployment automation for catered by me"""
    print("🚀 Asking Otto to deploy catered by me and fix any errors...")
    print()
    
    # Load config
    config = load_config()
    context = SkillContext(config=config, logger=logger)
    skills = get_all_skills()
    
    # Create deployment task
    task = Task(
        id=str(uuid.uuid4()),
        type="deployment.deploy_and_fix",
        payload={
            "project_path": "catered_by_me",
            "project_name": "catered-by-me",
            "max_iterations": 5
        },
        source="cli",
        status=TaskStatus.PENDING
    )
    
    print(f"📋 Task: {task.type}")
    print(f"   Project: {task.payload['project_name']}")
    print(f"   Max iterations: {task.payload['max_iterations']}")
    print()
    print("⏳ Running deployment automation...")
    print()
    
    # Run the task
    results = run_tasks([task], skills, context)
    result = results[0]
    
    # Print results
    print("=" * 60)
    if result.success:
        print(f"✅ SUCCESS: {result.message}")
        print()
        if result.data:
            iterations = result.data.get("iterations", 0)
            print(f"   Completed in {iterations} iteration(s)")
            print()
            
            # Print iteration results
            results_list = result.data.get("results", [])
            if results_list:
                print("   Iteration Summary:")
                for res in results_list:
                    print(f"   - {res}")
                print()
            
            # Print deployment details
            if result.data.get("render"):
                render = result.data["render"]
                print(f"   Render: {render.get('status', 'unknown')}")
            if result.data.get("vercel"):
                vercel = result.data["vercel"]
                print(f"   Vercel: {vercel.get('status', 'unknown')}")
                if vercel.get("url"):
                    print(f"   URL: {vercel['url']}")
    else:
        print(f"❌ FAILED: {result.message}")
        print()
        if result.data:
            iterations = result.data.get("iterations", 0)
            print(f"   Attempted {iterations} iteration(s)")
            print()
            
            # Print what went wrong
            if result.data.get("render"):
                render = result.data["render"]
                if not render.get("success"):
                    print(f"   Render Error: {render.get('message', 'Unknown error')}")
            if result.data.get("vercel"):
                vercel = result.data["vercel"]
                if not vercel.get("success"):
                    print(f"   Vercel Error: {vercel.get('message', 'Unknown error')}")
                    if vercel.get("errors"):
                        print("   Errors detected:")
                        for error in vercel["errors"]:
                            print(f"     - {error.get('type', 'unknown')}: {error.get('variable', '')}")
    
    print("=" * 60)
    
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()

