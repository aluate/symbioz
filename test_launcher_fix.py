"""
Script to have Otto diagnose and fix the Symbioz launcher
"""

import sys
import os
from pathlib import Path

# Add apps/otto to path
sys.path.insert(0, str(Path(__file__).parent / "apps" / "otto"))

from otto.core.models import Task, TaskStatus
from otto.core.skill_base import SkillContext
from otto.core.runner import run_tasks
from otto.config import load_config
from otto.skills import get_all_skills
from otto.core.logging_utils import get_logger
import uuid

logger = get_logger(__name__)

def main():
    """Have Otto diagnose and fix the launcher"""
    print("=" * 60)
    print("Otto Launcher Diagnostic & Fix")
    print("=" * 60)
    print()
    
    # Load config
    config = load_config()
    context = SkillContext(config=config, logger=logger)
    skills = get_all_skills()
    
    # Step 1: Diagnose
    print("[1/3] Diagnosing launcher issues...")
    diagnose_task = Task(
        id=str(uuid.uuid4()),
        type="launcher_diagnostic",
        payload={"action": "diagnose"},
        source="cli",
        status=TaskStatus.PENDING
    )
    
    results = run_tasks([diagnose_task], skills, context)
    diagnose_result = results[0]
    
    if diagnose_result.success:
        print(f"✅ Diagnosis: {diagnose_result.message}")
    else:
        print(f"⚠️  Diagnosis: {diagnose_result.message}")
    
    if diagnose_result.data:
        issues = diagnose_result.data.get("issues", [])
        if issues:
            print(f"\nFound {len(issues)} issue(s):")
            for issue in issues:
                print(f"  - [{issue.get('type')}] {issue.get('message')}")
                if issue.get('suggestion'):
                    print(f"    → {issue.get('suggestion')}")
    
    print()
    
    # Step 2: Fix
    print("[2/3] Applying fixes...")
    fix_task = Task(
        id=str(uuid.uuid4()),
        type="launcher_diagnostic",
        payload={"action": "fix"},
        source="cli",
        status=TaskStatus.PENDING
    )
    
    results = run_tasks([fix_task], skills, context)
    fix_result = results[0]
    
    if fix_result.success:
        print(f"✅ Fix: {fix_result.message}")
        if fix_result.data and fix_result.data.get("fixes_applied"):
            fixes = fix_result.data["fixes_applied"]
            print(f"   Applied {len(fixes)} fix(es):")
            for fix in fixes:
                print(f"     - {fix}")
    else:
        print(f"⚠️  Fix: {fix_result.message}")
    
    print()
    
    # Step 3: Test
    print("[3/3] Testing launcher...")
    test_task = Task(
        id=str(uuid.uuid4()),
        type="launcher_diagnostic",
        payload={"action": "test"},
        source="cli",
        status=TaskStatus.PENDING
    )
    
    results = run_tasks([test_task], skills, context)
    test_result = results[0]
    
    if test_result.success:
        print(f"✅ Test: {test_result.message}")
        if test_result.data and test_result.data.get("test_results"):
            for test in test_result.data["test_results"]:
                status = "✓" if test.get("ok") else "✗"
                print(f"   {status} {test.get('test')}")
                if not test.get("ok") and test.get("error"):
                    print(f"     Error: {test.get('error')[:200]}")
    else:
        print(f"❌ Test: {test_result.message}")
        if test_result.data and test_result.data.get("error"):
            print(f"   Error: {test_result.data['error'][:500]}")
    
    print()
    print("=" * 60)
    if test_result.success:
        print("✅ Launcher is ready to use!")
        print("   Run LAUNCH_SYMBIOZ.bat to start the game.")
    else:
        print("⚠️  Some issues remain. Check the output above.")
    print("=" * 60)

if __name__ == "__main__":
    main()



