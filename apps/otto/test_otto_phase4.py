"""
Phase 4 Test Suite - Memory History, Expiration, Links, and Search
Phase 4 — CONTROL_OTTO_PHASE4_MEMORY_UI_AND_MAINTENANCE.md

Run this script to test Otto's Phase 4 memory features.

Prerequisites:
- Life OS backend running on http://localhost:8000
- Otto API running on http://localhost:8001
- Database initialized (SQLite, migrations applied)
"""

import httpx
import json
import sys
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

# API URLs
LIFE_OS_API_URL = "http://localhost:8000"
OTTO_API_URL = "http://localhost:8001"

# Test results
test_results = []


def log_test(name: str, passed: bool, message: str = "", details: Optional[Dict] = None):
    """Log a test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    test_results.append({
        "name": name,
        "passed": passed,
        "message": message,
        "details": details or {}
    })
    print(f"{status}: {name}")
    if message:
        print(f"   {message}")
    if details:
        for key, value in details.items():
            print(f"   {key}: {value}")


def check_services() -> bool:
    """Check if required services are running"""
    print("=== Checking Services ===")
    services_ok = True
    
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{LIFE_OS_API_URL}/health")
            if response.status_code == 200:
                print("✅ Life OS Backend: Running")
            else:
                print(f"❌ Life OS Backend: Unexpected status {response.status_code}")
                services_ok = False
    except Exception as e:
        print(f"❌ Life OS Backend: Not reachable ({str(e)})")
        services_ok = False
    
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{OTTO_API_URL}/health")
            if response.status_code == 200:
                print("✅ Otto API: Running")
            else:
                print(f"❌ Otto API: Unexpected status {response.status_code}")
                services_ok = False
    except Exception as e:
        print(f"❌ Otto API: Not reachable ({str(e)})")
        services_ok = False
    
    if not services_ok:
        print("\n❌ Required services are not running. Please start:")
        print("   - Life OS Backend (http://localhost:8000)")
        print("   - Otto API (http://localhost:8001)")
    
    return services_ok


def test_memory_history():
    """Test memory history creation and retrieval"""
    print("\n=== Test: Memory History ===")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            # 1. Create a memory
            create_response = client.post(
                f"{LIFE_OS_API_URL}/otto/memory",
                json={
                    "category": "test",
                    "content": "Original content for history test",
                    "tags": ["test", "history"],
                    "source": "test"
                }
            )
            
            if create_response.status_code != 200:
                log_test("Memory History - Create", False, f"Failed to create memory: {create_response.status_code}")
                return
            
            memory = create_response.json()
            memory_id = memory["id"]
            original_version = memory["version"]
            
            log_test("Memory History - Create", True, f"Created memory {memory_id} (v{original_version})")
            
            # 2. Update the memory (should create history)
            update_response = client.patch(
                f"{LIFE_OS_API_URL}/otto/memory/{memory_id}",
                json={
                    "content": "Updated content for history test",
                    "tags": ["test", "history", "updated"]
                }
            )
            
            if update_response.status_code != 200:
                log_test("Memory History - Update", False, f"Failed to update memory: {update_response.status_code}")
                return
            
            updated_memory = update_response.json()
            new_version = updated_memory["version"]
            
            if new_version != original_version + 1:
                log_test("Memory History - Version Increment", False, 
                        f"Version should be {original_version + 1}, got {new_version}")
            else:
                log_test("Memory History - Version Increment", True, f"Version incremented to {new_version}")
            
            # 3. Get history
            history_response = client.get(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}/history")
            
            if history_response.status_code != 200:
                log_test("Memory History - Retrieve", False, f"Failed to get history: {history_response.status_code}")
                return
            
            history = history_response.json()
            
            if len(history) == 0:
                log_test("Memory History - Retrieve", False, "No history entries found")
            else:
                log_test("Memory History - Retrieve", True, f"Found {len(history)} history entry(ies)")
                
                # Check that history contains original version
                original_found = any(h["version"] == original_version for h in history)
                if original_found:
                    log_test("Memory History - Original Preserved", True, "Original version found in history")
                else:
                    log_test("Memory History - Original Preserved", False, "Original version not found in history")
            
            # 4. Get specific version
            version_response = client.get(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}/history/{original_version}")
            
            if version_response.status_code != 200:
                log_test("Memory History - Get Version", False, f"Failed to get version: {version_response.status_code}")
            else:
                version_data = version_response.json()
                if version_data["content"] == "Original content for history test":
                    log_test("Memory History - Get Version", True, "Correct version content retrieved")
                else:
                    log_test("Memory History - Get Version", False, "Incorrect version content")
            
            # Cleanup
            client.delete(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}")
            
    except Exception as e:
        log_test("Memory History - Exception", False, f"Error: {str(e)}")


def test_memory_expiration():
    """Test memory expiration and stale marking"""
    print("\n=== Test: Memory Expiration ===")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            # 1. Create a memory
            create_response = client.post(
                f"{LIFE_OS_API_URL}/otto/memory",
                json={
                    "category": "test",
                    "content": "Memory for expiration test",
                    "tags": ["test", "expiration"],
                    "source": "test"
                }
            )
            
            if create_response.status_code != 200:
                log_test("Memory Expiration - Create", False, f"Failed to create memory: {create_response.status_code}")
                return
            
            memory = create_response.json()
            memory_id = memory["id"]
            
            log_test("Memory Expiration - Create", True, f"Created memory {memory_id}")
            
            # 2. Set expiration
            expires_at = (datetime.utcnow() + timedelta(days=7)).isoformat()
            action_response = client.post(
                f"{LIFE_OS_API_URL}/otto/actions",
                json={
                    "actions": [{
                        "type": "memory.set_expiration",
                        "payload": {
                            "memory_id": memory_id,
                            "expires_at": expires_at
                        }
                    }]
                }
            )
            
            if action_response.status_code != 200:
                log_test("Memory Expiration - Set Expiration", False, 
                        f"Failed to set expiration: {action_response.status_code}")
            else:
                # Verify expiration was set
                get_response = client.get(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}")
                if get_response.status_code == 200:
                    memory_data = get_response.json()
                    if memory_data.get("expires_at"):
                        log_test("Memory Expiration - Set Expiration", True, "Expiration date set")
                    else:
                        log_test("Memory Expiration - Set Expiration", False, "Expiration date not set")
            
            # 3. Mark as stale
            mark_stale_response = client.post(
                f"{LIFE_OS_API_URL}/otto/actions",
                json={
                    "actions": [{
                        "type": "memory.mark_stale",
                        "payload": {
                            "memory_id": memory_id,
                            "reason": "Test reason"
                        }
                    }]
                }
            )
            
            if mark_stale_response.status_code != 200:
                log_test("Memory Expiration - Mark Stale", False, 
                        f"Failed to mark stale: {mark_stale_response.status_code}")
            else:
                # Verify stale was set
                get_response = client.get(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}")
                if get_response.status_code == 200:
                    memory_data = get_response.json()
                    if memory_data.get("is_stale") == True:
                        log_test("Memory Expiration - Mark Stale", True, "Memory marked as stale")
                    else:
                        log_test("Memory Expiration - Mark Stale", False, "Memory not marked as stale")
                    
                    if memory_data.get("stale_reason") == "Test reason":
                        log_test("Memory Expiration - Stale Reason", True, "Stale reason set correctly")
                    else:
                        log_test("Memory Expiration - Stale Reason", False, "Stale reason not set")
            
            # Cleanup
            client.delete(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}")
            
    except Exception as e:
        log_test("Memory Expiration - Exception", False, f"Error: {str(e)}")


def test_memory_links():
    """Test memory link creation and retrieval"""
    print("\n=== Test: Memory Links ===")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            # 1. Create a memory
            create_response = client.post(
                f"{LIFE_OS_API_URL}/otto/memory",
                json={
                    "category": "test",
                    "content": "Memory for link test",
                    "tags": ["test", "links"],
                    "source": "test"
                }
            )
            
            if create_response.status_code != 200:
                log_test("Memory Links - Create Memory", False, f"Failed to create memory: {create_response.status_code}")
                return
            
            memory = create_response.json()
            memory_id = memory["id"]
            
            log_test("Memory Links - Create Memory", True, f"Created memory {memory_id}")
            
            # 2. Create a link to a bill (simulated)
            link_response = client.post(
                f"{LIFE_OS_API_URL}/otto/memory/{memory_id}/links",
                json={
                    "target_type": "bill",
                    "target_id": 999,  # Simulated bill ID
                    "relationship_type": "applies_to",
                    "notes": "Test link"
                }
            )
            
            if link_response.status_code != 200:
                log_test("Memory Links - Create Link", False, f"Failed to create link: {link_response.status_code}")
            else:
                link = link_response.json()
                log_test("Memory Links - Create Link", True, f"Created link {link['id']}")
            
            # 3. Get links
            links_response = client.get(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}/links")
            
            if links_response.status_code != 200:
                log_test("Memory Links - Get Links", False, f"Failed to get links: {links_response.status_code}")
            else:
                links = links_response.json()
                if len(links) > 0:
                    log_test("Memory Links - Get Links", True, f"Found {len(links)} link(s)")
                else:
                    log_test("Memory Links - Get Links", False, "No links found")
            
            # 4. Delete link
            if link_response.status_code == 200:
                link_id = link_response.json()["id"]
                delete_response = client.delete(f"{LIFE_OS_API_URL}/otto/memory/links/{link_id}")
                
                if delete_response.status_code == 200:
                    log_test("Memory Links - Delete Link", True, "Link deleted")
                else:
                    log_test("Memory Links - Delete Link", False, f"Failed to delete: {delete_response.status_code}")
            
            # Cleanup
            client.delete(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}")
            
    except Exception as e:
        log_test("Memory Links - Exception", False, f"Error: {str(e)}")


def test_memory_search():
    """Test memory search functionality"""
    print("\n=== Test: Memory Search ===")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            # 1. Create test memories
            test_memories = []
            for i in range(3):
                create_response = client.post(
                    f"{LIFE_OS_API_URL}/otto/memory",
                    json={
                        "category": "test",
                        "content": f"Test memory {i} with unique content XYZ{i}",
                        "tags": ["test", f"tag{i}"],
                        "source": "test"
                    }
                )
                if create_response.status_code == 200:
                    test_memories.append(create_response.json())
            
            if len(test_memories) == 0:
                log_test("Memory Search - Create Test Data", False, "Failed to create test memories")
                return
            
            log_test("Memory Search - Create Test Data", True, f"Created {len(test_memories)} test memories")
            
            # 2. Search by text
            search_response = client.get(
                f"{LIFE_OS_API_URL}/otto/memory/search",
                params={"q": "XYZ1", "limit": 10}
            )
            
            if search_response.status_code != 200:
                log_test("Memory Search - Text Search", False, f"Failed to search: {search_response.status_code}")
            else:
                results = search_response.json()
                if len(results) > 0:
                    log_test("Memory Search - Text Search", True, f"Found {len(results)} result(s)")
                else:
                    log_test("Memory Search - Text Search", False, "No results found")
            
            # 3. Search by category
            category_response = client.get(
                f"{LIFE_OS_API_URL}/otto/memory/search",
                params={"category": "test", "limit": 10}
            )
            
            if category_response.status_code != 200:
                log_test("Memory Search - Category Filter", False, f"Failed to filter: {category_response.status_code}")
            else:
                results = category_response.json()
                if len(results) >= len(test_memories):
                    log_test("Memory Search - Category Filter", True, f"Found {len(results)} result(s)")
                else:
                    log_test("Memory Search - Category Filter", False, f"Expected at least {len(test_memories)}, got {len(results)}")
            
            # 4. Search by stale status
            stale_response = client.get(
                f"{LIFE_OS_API_URL}/otto/memory/search",
                params={"is_stale": False, "limit": 10}
            )
            
            if stale_response.status_code != 200:
                log_test("Memory Search - Stale Filter", False, f"Failed to filter: {stale_response.status_code}")
            else:
                results = stale_response.json()
                log_test("Memory Search - Stale Filter", True, f"Found {len(results)} non-stale result(s)")
            
            # Cleanup
            for memory in test_memories:
                client.delete(f"{LIFE_OS_API_URL}/otto/memory/{memory['id']}")
            
    except Exception as e:
        log_test("Memory Search - Exception", False, f"Error: {str(e)}")


def test_memory_search_action():
    """Test memory.search action via Otto API"""
    print("\n=== Test: Memory Search Action ===")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            # Create a test memory first
            create_response = client.post(
                f"{LIFE_OS_API_URL}/otto/memory",
                json={
                    "category": "test",
                    "content": "Search action test content ABC123",
                    "tags": ["test", "search_action"],
                    "source": "test"
                }
            )
            
            if create_response.status_code != 200:
                log_test("Memory Search Action - Create", False, "Failed to create test memory")
                return
            
            memory_id = create_response.json()["id"]
            
            # Call memory.search via Otto API
            search_response = client.post(
                f"{OTTO_API_URL}/task",
                json={
                    "type": "memory.search",
                    "payload": {
                        "q": "ABC123",
                        "limit": 10
                    }
                }
            )
            
            if search_response.status_code != 200:
                log_test("Memory Search Action - Call", False, f"Failed to call action: {search_response.status_code}")
            else:
                result = search_response.json()
                # Otto API returns "status" not "success", and "result" not "data"
                if result.get("status") == "success":
                    log_test("Memory Search Action - Call", True, "Search action succeeded")
                    result_data = result.get("result", {})
                    if isinstance(result_data, dict):
                        count = result_data.get("count", len(result_data.get("memories", [])))
                    else:
                        count = 0
                    if count > 0:
                        log_test("Memory Search Action - Results", True, "Search returned results")
                    else:
                        log_test("Memory Search Action - Results", False, "Search returned no results")
                else:
                    log_test("Memory Search Action - Call", False, f"Action failed: {result.get('message')}")
            
            # Cleanup
            client.delete(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}")
            
    except Exception as e:
        log_test("Memory Search Action - Exception", False, f"Error: {str(e)}")


def generate_report() -> Dict[str, Any]:
    """Generate test report"""
    total_tests = len(test_results)
    passed_tests = sum(1 for r in test_results if r["passed"])
    failed_tests = total_tests - passed_tests
    
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "summary": {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
        },
        "results": test_results,
        "failed_tests": [r for r in test_results if not r["passed"]],
        "passed_tests": [r for r in test_results if r["passed"]]
    }
    
    return report


def print_report(report: Dict[str, Any]):
    """Print formatted test report"""
    print("\n" + "=" * 60)
    print("PHASE 4 TEST REPORT")
    print("=" * 60)
    print(f"\nTimestamp: {report['timestamp']}")
    print(f"\nSummary:")
    print(f"  Total Tests: {report['summary']['total']}")
    print(f"  Passed: {report['summary']['passed']} ✅")
    print(f"  Failed: {report['summary']['failed']} ❌")
    print(f"  Pass Rate: {report['summary']['pass_rate']:.1f}%")
    
    if report['failed_tests']:
        print(f"\n❌ FAILED TESTS ({len(report['failed_tests'])}):")
        for test in report['failed_tests']:
            print(f"  - {test['name']}")
            if test['message']:
                print(f"    {test['message']}")
    
    if report['passed_tests']:
        print(f"\n✅ PASSED TESTS ({len(report['passed_tests'])}):")
        for test in report['passed_tests']:
            print(f"  - {test['name']}")
    
    print("\n" + "=" * 60)


def main():
    """Run all Phase 4 tests"""
    print("=" * 60)
    print("Phase 4 Test Suite - Memory History, Expiration, Links, Search")
    print("=" * 60)
    
    if not check_services():
        print("\n⚠️  Services not running. Cannot run tests.")
        print("   Please start services and run again.")
        sys.exit(1)
    
    # Run tests
    test_memory_history()
    test_memory_expiration()
    test_memory_links()
    test_memory_search()
    test_memory_search_action()
    
    # Generate and print report
    report = generate_report()
    print_report(report)
    
    # Save report to file
    report_file = "PHASE4_TEST_REPORT.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n📄 Full report saved to: {report_file}")
    
    # Exit with appropriate code
    if report['summary']['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

