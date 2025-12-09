"""
Master Test Runner - Phase 3 + Phase 4
Runs all memory system tests and generates comprehensive report

Usage:
    python run_tests_and_report.py

Prerequisites:
    - Life OS backend running on http://localhost:8000
    - Otto API running on http://localhost:8001
    - Database initialized (SQLite, migrations applied)

To start services:
    - Run START_OTTO_WINDOWS.bat from repo root
    - Or manually start:
        - Life OS Backend: cd apps/life_os/backend && python -m uvicorn main:app --reload --port 8000
        - Otto API: cd apps/otto && python -m otto.cli server
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Import test modules
try:
    from test_otto_phase3 import (
        check_services as check_services_phase3,
        test_memory_api_create,
        test_memory_api_retrieve,
        test_memory_api_list_filters,
        test_memory_api_update,
        test_memory_api_usage_tracking,
        test_memory_skill_remember,
        test_memory_skill_recall,
        test_memory_skill_lookup,
        test_memory_skill_update,
        test_memory_skill_delete,
        test_results as phase3_results
    )
except ImportError as e:
    print(f"⚠️  Could not import Phase 3 tests: {e}")
    phase3_results = []

try:
    from test_otto_phase4 import (
        check_services as check_services_phase4,
        test_memory_history,
        test_memory_expiration,
        test_memory_links,
        test_memory_search,
        test_memory_search_action,
        test_results as phase4_results
    )
except ImportError as e:
    print(f"⚠️  Could not import Phase 4 tests: {e}")
    phase4_results = []


def check_services() -> bool:
    """Check if required services are running"""
    print("=" * 70)
    print("CHECKING SERVICES")
    print("=" * 70)
    
    services_ok = True
    
    # Check Life OS Backend
    try:
        import httpx
        with httpx.Client(timeout=5.0) as client:
            response = client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("[OK] Life OS Backend: Running on http://localhost:8000")
            else:
                print(f"[FAIL] Life OS Backend: Unexpected status {response.status_code}")
                services_ok = False
    except Exception as e:
        print(f"[FAIL] Life OS Backend: Not reachable ({str(e)})")
        services_ok = False
    
    # Check Otto API
    try:
        import httpx
        with httpx.Client(timeout=5.0) as client:
            response = client.get("http://localhost:8001/health")
            if response.status_code == 200:
                print("[OK] Otto API: Running on http://localhost:8001")
            else:
                print(f"[FAIL] Otto API: Unexpected status {response.status_code}")
                services_ok = False
    except Exception as e:
        print(f"[FAIL] Otto API: Not reachable ({str(e)})")
        services_ok = False
    
    if not services_ok:
        print("\n" + "=" * 70)
        print("⚠️  SERVICES NOT RUNNING")
        print("=" * 70)
        print("\nTo start services:")
        print("  1. Run START_OTTO_WINDOWS.bat from repo root, OR")
        print("  2. Manually start:")
        print("     - Life OS Backend: cd apps/life_os/backend && python -m uvicorn main:app --reload --port 8000")
        print("     - Otto API: cd apps/otto && python -m otto.cli server")
        print("\nThen run this script again.")
        print("=" * 70)
    
    return services_ok


def run_phase3_tests():
    """Run Phase 3 tests"""
    print("\n" + "=" * 70)
    print("PHASE 3 TESTS - Memory API & Skills")
    print("=" * 70)
    
    # Clear previous results
    phase3_results.clear()
    
    try:
        # Run Phase 3 tests
        memory_id = test_memory_api_create()
        if memory_id:
            test_memory_api_retrieve(memory_id)
            test_memory_api_list_filters()
            test_memory_api_update(memory_id)
            test_memory_api_usage_tracking(memory_id)
            test_memory_skill_remember()
            test_memory_skill_recall(memory_id)
            test_memory_skill_lookup()
            test_memory_skill_update(memory_id)
            test_memory_skill_delete(memory_id)
    except Exception as e:
        print(f"❌ Error running Phase 3 tests: {str(e)}")
        phase3_results.append({
            "name": "Phase 3 - Test Execution",
            "passed": False,
            "message": f"Error: {str(e)}"
        })


def run_phase4_tests():
    """Run Phase 4 tests"""
    print("\n" + "=" * 70)
    print("PHASE 4 TESTS - History, Expiration, Links, Search")
    print("=" * 70)
    
    # Clear previous results
    phase4_results.clear()
    
    try:
        # Run Phase 4 tests
        test_memory_history()
        test_memory_expiration()
        test_memory_links()
        test_memory_search()
        test_memory_search_action()
    except Exception as e:
        print(f"❌ Error running Phase 4 tests: {str(e)}")
        phase4_results.append({
            "name": "Phase 4 - Test Execution",
            "passed": False,
            "message": f"Error: {str(e)}"
        })


def generate_comprehensive_report():
    """Generate comprehensive test report"""
    all_results = []
    
    # Add Phase 3 results
    for result in phase3_results:
        all_results.append({
            **result,
            "phase": "Phase 3",
            "category": categorize_test(result["name"])
        })
    
    # Add Phase 4 results
    for result in phase4_results:
        all_results.append({
            **result,
            "phase": "Phase 4",
            "category": categorize_test(result["name"])
        })
    
    # Calculate statistics
    total = len(all_results)
    passed = sum(1 for r in all_results if r["passed"])
    failed = total - passed
    
    phase3_total = sum(1 for r in all_results if r["phase"] == "Phase 3")
    phase3_passed = sum(1 for r in all_results if r["phase"] == "Phase 3" and r["passed"])
    
    phase4_total = sum(1 for r in all_results if r["phase"] == "Phase 4")
    phase4_passed = sum(1 for r in all_results if r["phase"] == "Phase 4" and r["passed"])
    
    # Group by category
    categories = {}
    for result in all_results:
        cat = result["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "passed": 0, "failed": 0, "tests": []}
        categories[cat]["total"] += 1
        if result["passed"]:
            categories[cat]["passed"] += 1
        else:
            categories[cat]["failed"] += 1
        categories[cat]["tests"].append(result)
    
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "phase3": {
                "total": phase3_total,
                "passed": phase3_passed,
                "failed": phase3_total - phase3_passed,
                "pass_rate": (phase3_passed / phase3_total * 100) if phase3_total > 0 else 0
            },
            "phase4": {
                "total": phase4_total,
                "passed": phase4_passed,
                "failed": phase4_total - phase4_passed,
                "pass_rate": (phase4_passed / phase4_total * 100) if phase4_total > 0 else 0
            }
        },
        "categories": categories,
        "failed_tests": [r for r in all_results if not r["passed"]],
        "passed_tests": [r for r in all_results if r["passed"]],
        "all_results": all_results
    }
    
    return report


def categorize_test(test_name: str) -> str:
    """Categorize test by name"""
    name_lower = test_name.lower()
    
    if "api" in name_lower or "create" in name_lower or "retrieve" in name_lower or "update" in name_lower or "delete" in name_lower:
        return "API Operations"
    elif "skill" in name_lower:
        return "Skill Integration"
    elif "history" in name_lower:
        return "Memory History"
    elif "expiration" in name_lower or "stale" in name_lower:
        return "Expiration & Maintenance"
    elif "link" in name_lower:
        return "Memory Links"
    elif "search" in name_lower:
        return "Search"
    elif "usage" in name_lower:
        return "Usage Tracking"
    else:
        return "Other"


def print_report(report: Dict):
    """Print formatted test report"""
    print("\n" + "=" * 70)
    print("COMPREHENSIVE TEST REPORT")
    print("=" * 70)
    print(f"\nTimestamp: {report['timestamp']}")
    
    # Overall summary
    print(f"\n{'=' * 70}")
    print("OVERALL SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Total Tests: {report['summary']['total']}")
    print(f"  Passed: {report['summary']['passed']} ✅")
    print(f"  Failed: {report['summary']['failed']} ❌")
    print(f"  Pass Rate: {report['summary']['pass_rate']:.1f}%")
    
    # Phase breakdown
    print(f"\n{'=' * 70}")
    print("PHASE BREAKDOWN")
    print(f"{'=' * 70}")
    print(f"\nPhase 3 (Memory API & Skills):")
    print(f"  Total: {report['summary']['phase3']['total']}")
    print(f"  Passed: {report['summary']['phase3']['passed']} ✅")
    print(f"  Failed: {report['summary']['phase3']['failed']} ❌")
    print(f"  Pass Rate: {report['summary']['phase3']['pass_rate']:.1f}%")
    
    print(f"\nPhase 4 (History, Expiration, Links, Search):")
    print(f"  Total: {report['summary']['phase4']['total']}")
    print(f"  Passed: {report['summary']['phase4']['passed']} ✅")
    print(f"  Failed: {report['summary']['phase4']['failed']} ❌")
    print(f"  Pass Rate: {report['summary']['phase4']['pass_rate']:.1f}%")
    
    # Category breakdown
    print(f"\n{'=' * 70}")
    print("CATEGORY BREAKDOWN")
    print(f"{'=' * 70}")
    for category, stats in report['categories'].items():
        pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"\n{category}:")
        print(f"  Total: {stats['total']}")
        print(f"  Passed: {stats['passed']} ✅")
        print(f"  Failed: {stats['failed']} ❌")
        print(f"  Pass Rate: {pass_rate:.1f}%")
    
    # Failed tests
    if report['failed_tests']:
        print(f"\n{'=' * 70}")
        print(f"❌ FAILED TESTS ({len(report['failed_tests'])})")
        print(f"{'=' * 70}")
        for test in report['failed_tests']:
            print(f"\n  [{test['phase']}] {test['name']}")
            if test.get('message'):
                print(f"    {test['message']}")
            if test.get('details'):
                for key, value in test['details'].items():
                    print(f"    {key}: {value}")
    
    # Passed tests summary
    if report['passed_tests']:
        print(f"\n{'=' * 70}")
        print(f"✅ PASSED TESTS ({len(report['passed_tests'])})")
        print(f"{'=' * 70}")
        for test in report['passed_tests']:
            print(f"  [{test['phase']}] {test['name']}")
    
    print("\n" + "=" * 70)


def save_report(report: Dict, filename: str = "TEST_REPORT.json"):
    """Save report to JSON file"""
    report_path = Path(filename)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    return report_path


def generate_cleanup_plan(report: Dict) -> Dict:
    """Generate cleanup plan based on test failures"""
    cleanup_plan = {
        "timestamp": datetime.utcnow().isoformat(),
        "failed_tests": len(report['failed_tests']),
        "actions": []
    }
    
    # Analyze failures and suggest fixes
    for test in report['failed_tests']:
        test_name = test['name'].lower()
        message = test.get('message', '').lower()
        
        action = {
            "test": test['name'],
            "phase": test.get('phase', 'Unknown'),
            "issue": test.get('message', 'Unknown error'),
            "suggested_fix": []
        }
        
        # Pattern matching for common issues
        if "not reachable" in message or "connection" in message:
            action["suggested_fix"].append("Check that services are running (Life OS Backend on :8000, Otto API on :8001)")
            action["suggested_fix"].append("Verify network connectivity and firewall settings")
        elif "status" in message and "404" in message:
            action["suggested_fix"].append("Check that endpoint exists in API")
            action["suggested_fix"].append("Verify database migrations are applied")
        elif "status" in message and "500" in message:
            action["suggested_fix"].append("Check server logs for errors")
            action["suggested_fix"].append("Verify database schema matches models")
        elif "history" in test_name:
            action["suggested_fix"].append("Verify OttoMemoryHistory model exists")
            action["suggested_fix"].append("Check that history creation happens in update/delete handlers")
        elif "expiration" in test_name or "stale" in test_name:
            action["suggested_fix"].append("Verify expiration fields exist on OttoMemory model")
            action["suggested_fix"].append("Check that actions are registered in ACTION_REGISTRY")
        elif "link" in test_name:
            action["suggested_fix"].append("Verify OttoMemoryLink model exists")
            action["suggested_fix"].append("Check that link endpoints are registered")
        elif "search" in test_name:
            action["suggested_fix"].append("Verify search endpoint exists")
            action["suggested_fix"].append("Check that memory.search action is registered")
        
        cleanup_plan["actions"].append(action)
    
    return cleanup_plan


def main():
    """Main test runner"""
    print("=" * 70)
    print("OTTO MEMORY SYSTEM - COMPREHENSIVE TEST RUNNER")
    print("=" * 70)
    print("\nThis will run:")
    print("  - Phase 3 tests (Memory API & Skills)")
    print("  - Phase 4 tests (History, Expiration, Links, Search)")
    print("\nGenerating comprehensive report...")
    
    # Check services
    if not check_services():
        print("\n❌ Cannot run tests - services not running.")
        sys.exit(1)
    
    # Run tests
    print("\n" + "=" * 70)
    print("RUNNING TESTS")
    print("=" * 70)
    
    run_phase3_tests()
    run_phase4_tests()
    
    # Generate report
    print("\n" + "=" * 70)
    print("GENERATING REPORT")
    print("=" * 70)
    
    report = generate_comprehensive_report()
    print_report(report)
    
    # Save report
    report_file = save_report(report, "TEST_REPORT.json")
    print(f"\n📄 Full report saved to: {report_file}")
    
    # Generate cleanup plan if there are failures
    if report['summary']['failed'] > 0:
        cleanup_plan = generate_cleanup_plan(report)
        cleanup_file = save_report(cleanup_plan, "CLEANUP_PLAN.json")
        print(f"📋 Cleanup plan saved to: {cleanup_file}")
        print("\n⚠️  Some tests failed. Review CLEANUP_PLAN.json for suggested fixes.")
    else:
        print("\n🎉 All tests passed!")
    
    # Exit with appropriate code
    sys.exit(0 if report['summary']['failed'] == 0 else 1)


if __name__ == "__main__":
    main()

