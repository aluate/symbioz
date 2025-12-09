#!/usr/bin/env python3
"""
Deploy Corporate Crashout using Otto's deployment automation skill.
This directly invokes Otto without needing the API server.
"""

import sys
import uuid
from pathlib import Path

# Force UTF-8 output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add apps/otto to path
workspace_root = Path(__file__).parent
sys.path.insert(0, str(workspace_root / "apps" / "otto"))

print("=" * 60)
print("🚀 Deploying Corporate Crashout with Otto")
print("=" * 60)
print()

try:
    from otto.config import load_config
    from otto.core.models import Task, TaskStatus
    from otto.core.skill_base import SkillContext
    from otto.core.runner import run_tasks
    from otto.core.logging_utils import get_logger
    from otto.skills import get_all_skills
    
    logger = get_logger(__name__)
    
    print("✅ Otto modules loaded")
    print()
    
    # Load config
    print("Loading Otto configuration...")
    config = load_config()
    context = SkillContext(config=config, logger=logger)
    skills = get_all_skills()
    
    print(f"✅ Found {len(skills)} skill(s)")
    print()
    
    # Create deployment task for Corporate Crashout
    print("Creating deployment task...")
    task = Task(
        id=str(uuid.uuid4()),
        type="corporate_crashout.deploy",  # Use the new task type we added
        payload={
            "project_path": "apps/corporate-crashout",
            "project_name": "achillies",
            "max_iterations": 5
        },
        source="cli",
        status=TaskStatus.PENDING
    )
    
    print(f"✅ Task created: {task.type}")
    print(f"   Project: {task.payload['project_name']}")
    print(f"   Max iterations: {task.payload['max_iterations']}")
    print()
    print("⏳ Running deployment automation...")
    print("=" * 60)
    print()
    
    # Run the task
    results = run_tasks([task], skills, context)
    result = results[0]
    
    # Print results
    print()
    print("=" * 60)
    if result.success:
        print(f"✅ SUCCESS: {result.message}")
        print("=" * 60)
        if result.data:
            print("\nDetails:")
            for key, value in result.data.items():
                if key == "output":
                    print(f"\n{value}")
                else:
                    print(f"  {key}: {value}")
        print()
        print("🎉 Corporate Crashout deployment complete!")
        print("Check your site at: https://achillies.vercel.app")
    else:
        print(f"❌ FAILED: {result.message}")
        print("=" * 60)
        if result.data:
            print("\nError details:")
            for key, value in result.data.items():
                if key == "error":
                    print(f"\n{value}")
                elif key == "output":
                    print(f"\nOutput:\n{value}")
                else:
                    print(f"  {key}: {value}")
        print()
        print("⚠️  Deployment failed. Check the errors above.")
        sys.exit(1)
        
except ImportError as e:
    print(f"❌ ERROR: Could not import Otto modules: {e}")
    print()
    print("Make sure you're in the workspace root and Otto is installed:")
    print("  cd apps/otto")
    print("  pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
