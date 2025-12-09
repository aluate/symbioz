"""
Phase 3B Test Suite - Memory System Tests
Phase 3 Extension — CONTROL_OTTO_LONG_TERM_MEMORY.md

Run this script to test Otto's long-term memory system.

Prerequisites:
- Life OS backend running on http://localhost:8000
- Otto API running on http://localhost:8001
- Database initialized (SQLite, migrations applied)
"""

import httpx
import json
import sys
from typing import Dict, Any, Optional

# API URLs
LIFE_OS_API_URL = "http://localhost:8000"
OTTO_API_URL = "http://localhost:8001"

# Test results
test_results = []


def log_test(name: str, passed: bool, message: str = ""):
    """Log a test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    test_results.append({
        "name": name,
        "passed": passed,
        "message": message
    })
    print(f"{status}: {name}")
    if message:
        print(f"   {message}")


def test_memory_api_create():
    """Test creating a memory entry via API"""
    print("\n=== Test 1: Memory API - Create ===")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{LIFE_OS_API_URL}/otto/memory",
                json={
                    "category": "preference",
                    "content": "Default reminder pattern is 7 days before, 1 day before, and day-of.",
                    "tags": ["reminder", "pattern"],
                    "source": "user",
                    "confidence_score": 1.0
                }
            )
            
            if response.status_code == 200:
                memory = response.json()
                log_test("Create memory via API", True, f"Created memory ID {memory.get('id')}")
                return memory.get("id")
            else:
                log_test("Create memory via API", False, f"Status {response.status_code}: {response.text}")
                return None
    except Exception as e:
        log_test("Create memory via API", False, f"Exception: {str(e)}")
        return None


def test_memory_api_retrieve(memory_id: Optional[int]):
    """Test retrieving memory by ID"""
    print("\n=== Test 2: Memory API - Retrieve by ID ===")
    
    if not memory_id:
        log_test("Retrieve memory by ID", False, "No memory ID from previous test")
        return
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}")
            
            if response.status_code == 200:
                memory = response.json()
                if memory.get("id") == memory_id:
                    log_test("Retrieve memory by ID", True, f"Retrieved memory: {memory.get('content', '')[:50]}...")
                else:
                    log_test("Retrieve memory by ID", False, "Wrong memory returned")
            else:
                log_test("Retrieve memory by ID", False, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        log_test("Retrieve memory by ID", False, f"Exception: {str(e)}")


def test_memory_api_list_filters():
    """Test listing memories with filters"""
    print("\n=== Test 3: Memory API - List with Filters ===")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            # Test category filter
            response = client.get(
                f"{LIFE_OS_API_URL}/otto/memory",
                params={"category": "preference", "limit": 10}
            )
            
            if response.status_code == 200:
                memories = response.json()
                log_test("List memories by category", True, f"Found {len(memories)} memory(ies)")
                
                # Test tag filter
                response = client.get(
                    f"{LIFE_OS_API_URL}/otto/memory",
                    params={"tags": "reminder", "limit": 10}
                )
                
                if response.status_code == 200:
                    memories = response.json()
                    log_test("List memories by tag", True, f"Found {len(memories)} memory(ies)")
                else:
                    log_test("List memories by tag", False, f"Status {response.status_code}")
            else:
                log_test("List memories by category", False, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        log_test("List memories with filters", False, f"Exception: {str(e)}")


def test_memory_api_update(memory_id: Optional[int]):
    """Test updating a memory entry"""
    print("\n=== Test 4: Memory API - Update ===")
    
    if not memory_id:
        log_test("Update memory", False, "No memory ID from previous test")
        return
    
    try:
        with httpx.Client(timeout=10.0) as client:
            # Get current version
            get_response = client.get(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}")
            if get_response.status_code != 200:
                log_test("Update memory", False, "Could not retrieve memory to update")
                return
            
            current_version = get_response.json().get("version", 1)
            
            # Update memory
            response = client.patch(
                f"{LIFE_OS_API_URL}/otto/memory/{memory_id}",
                json={
                    "content": "Updated: Default reminder pattern is 7 days before, 1 day before, and day-of.",
                    "confidence_score": 0.9
                }
            )
            
            if response.status_code == 200:
                memory = response.json()
                new_version = memory.get("version", 0)
                
                if new_version == current_version + 1:
                    log_test("Update memory (version increment)", True, f"Version incremented: {current_version} → {new_version}")
                else:
                    log_test("Update memory (version increment)", False, f"Version did not increment correctly: {current_version} → {new_version}")
            else:
                log_test("Update memory", False, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        log_test("Update memory", False, f"Exception: {str(e)}")


def test_memory_api_usage_tracking(memory_id: Optional[int]):
    """Test marking memory as used"""
    print("\n=== Test 5: Memory API - Usage Tracking ===")
    
    if not memory_id:
        log_test("Usage tracking", False, "No memory ID from previous test")
        return
    
    try:
        with httpx.Client(timeout=10.0) as client:
            # Get current usage count
            get_response = client.get(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}")
            if get_response.status_code != 200:
                log_test("Usage tracking", False, "Could not retrieve memory")
                return
            
            current_count = get_response.json().get("usage_count", 0)
            
            # Mark as used
            response = client.post(
                f"{LIFE_OS_API_URL}/otto/memory/use",
                json={"id": memory_id}
            )
            
            if response.status_code == 200:
                # Check updated count
                get_response = client.get(f"{LIFE_OS_API_URL}/otto/memory/{memory_id}")
                if get_response.status_code == 200:
                    memory = get_response.json()
                    new_count = memory.get("usage_count", 0)
                    last_used = memory.get("last_used_at")
                    
                    if new_count == current_count + 1 and last_used:
                        log_test("Usage tracking (count increment)", True, f"Usage count: {current_count} → {new_count}")
                        log_test("Usage tracking (last_used_at)", True, f"last_used_at set: {last_used}")
                    else:
                        log_test("Usage tracking", False, f"Usage count or last_used_at not updated correctly")
                else:
                    log_test("Usage tracking", False, "Could not verify usage update")
            else:
                log_test("Usage tracking", False, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        log_test("Usage tracking", False, f"Exception: {str(e)}")


def test_memory_skill_remember():
    """Test OttoMemorySkill via Otto API - remember"""
    print("\n=== Test 6: OttoMemorySkill - remember ===")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{OTTO_API_URL}/task",
                json={
                    "type": "memory.remember",
                    "payload": {
                        "category": "preference",
                        "content": "Test memory from skill",
                        "tags": ["test"],
                        "source": "user"
                    },
                    "source": "test"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    actions = result.get("actions", [])
                    if actions and actions[0].get("type") == "memory.create":
                        log_test("Memory skill - remember", True, "Created memory.create action")
                    else:
                        log_test("Memory skill - remember", False, "No memory.create action in response")
                else:
                    log_test("Memory skill - remember", False, f"Status: {result.get('status')}")
            else:
                log_test("Memory skill - remember", False, f"HTTP {response.status_code}: {response.text}")
    except Exception as e:
        log_test("Memory skill - remember", False, f"Exception: {str(e)}")


def test_memory_skill_recall(memory_id: Optional[int]):
    """Test OttoMemorySkill via Otto API - recall"""
    print("\n=== Test 7: OttoMemorySkill - recall ===")
    
    if not memory_id:
        log_test("Memory skill - recall", False, "No memory ID from previous test")
        return
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{OTTO_API_URL}/task",
                json={
                    "type": "memory.recall",
                    "payload": {
                        "id": memory_id
                    },
                    "source": "test"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    data = result.get("result", {})
                    if data.get("memory"):
                        log_test("Memory skill - recall", True, f"Recalled memory: {data['memory'].get('content', '')[:50]}...")
                    else:
                        log_test("Memory skill - recall", False, "No memory in response")
                else:
                    log_test("Memory skill - recall", False, f"Status: {result.get('status')}")
            else:
                log_test("Memory skill - recall", False, f"HTTP {response.status_code}: {response.text}")
    except Exception as e:
        log_test("Memory skill - recall", False, f"Exception: {str(e)}")


def test_memory_skill_lookup():
    """Test OttoMemorySkill via Otto API - lookup"""
    print("\n=== Test 8: OttoMemorySkill - lookup ===")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{OTTO_API_URL}/task",
                json={
                    "type": "memory.lookup",
                    "payload": {
                        "category": "preference",
                        "tags": ["reminder"],
                        "limit": 10
                    },
                    "source": "test"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    data = result.get("result", {})
                    memories = data.get("memories", [])
                    log_test("Memory skill - lookup", True, f"Found {len(memories)} memory(ies)")
                else:
                    log_test("Memory skill - lookup", False, f"Status: {result.get('status')}")
            else:
                log_test("Memory skill - lookup", False, f"HTTP {response.status_code}: {response.text}")
    except Exception as e:
        log_test("Memory skill - lookup", False, f"Exception: {str(e)}")


def test_memory_skill_update(memory_id: Optional[int]):
    """Test OttoMemorySkill via Otto API - update"""
    print("\n=== Test 9: OttoMemorySkill - update ===")
    
    if not memory_id:
        log_test("Memory skill - update", False, "No memory ID from previous test")
        return
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{OTTO_API_URL}/task",
                json={
                    "type": "memory.update",
                    "payload": {
                        "id": memory_id,
                        "content": "Updated via skill test"
                    },
                    "source": "test"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    actions = result.get("actions", [])
                    if actions and actions[0].get("type") == "memory.update":
                        log_test("Memory skill - update", True, "Created memory.update action")
                    else:
                        log_test("Memory skill - update", False, "No memory.update action in response")
                else:
                    log_test("Memory skill - update", False, f"Status: {result.get('status')}")
            else:
                log_test("Memory skill - update", False, f"HTTP {response.status_code}: {response.text}")
    except Exception as e:
        log_test("Memory skill - update", False, f"Exception: {str(e)}")


def test_memory_skill_delete(memory_id: Optional[int]):
    """Test OttoMemorySkill via Otto API - delete"""
    print("\n=== Test 10: OttoMemorySkill - delete ===")
    
    if not memory_id:
        log_test("Memory skill - delete", False, "No memory ID from previous test")
        return
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{OTTO_API_URL}/task",
                json={
                    "type": "memory.delete",
                    "payload": {
                        "id": memory_id
                    },
                    "source": "test"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    actions = result.get("actions", [])
                    if actions and actions[0].get("type") == "memory.delete":
                        log_test("Memory skill - delete", True, "Created memory.delete action")
                    else:
                        log_test("Memory skill - delete", False, "No memory.delete action in response")
                else:
                    log_test("Memory skill - delete", False, f"Status: {result.get('status')}")
            else:
                log_test("Memory skill - delete", False, f"HTTP {response.status_code}: {response.text}")
    except Exception as e:
        log_test("Memory skill - delete", False, f"Exception: {str(e)}")


def check_services():
    """Check if required services are running"""
    print("=== Checking Services ===")
    
    services_ok = True
    
    # Check Life OS backend
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{LIFE_OS_API_URL}/health")
            if response.status_code == 200:
                print("✅ Life OS Backend: Running")
            else:
                print(f"❌ Life OS Backend: Status {response.status_code}")
                services_ok = False
    except Exception as e:
        print(f"❌ Life OS Backend: Not reachable ({str(e)})")
        services_ok = False
    
    # Check Otto API
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{OTTO_API_URL}/health")
            if response.status_code == 200:
                print("✅ Otto API: Running")
            else:
                print(f"❌ Otto API: Status {response.status_code}")
                services_ok = False
    except Exception as e:
        print(f"❌ Otto API: Not reachable ({str(e)})")
        services_ok = False
    
    return services_ok


def main():
    """Run all tests"""
    print("=" * 60)
    print("Phase 3B Test Suite - Otto Memory System")
    print("=" * 60)
    
    # Check services
    if not check_services():
        print("\n❌ Required services are not running. Please start:")
        print("   - Life OS Backend (http://localhost:8000)")
        print("   - Otto API (http://localhost:8001)")
        sys.exit(1)
    
    # Run tests
    memory_id = test_memory_api_create()
    test_memory_api_retrieve(memory_id)
    test_memory_api_list_filters()
    test_memory_api_update(memory_id)
    test_memory_api_usage_tracking(memory_id)
    test_memory_skill_remember()
    test_memory_skill_recall(memory_id)
    test_memory_skill_lookup()
    test_memory_skill_update(memory_id)
    test_memory_skill_delete(memory_id)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for r in test_results if r["passed"])
    total = len(test_results)
    
    for result in test_results:
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"{status}: {result['name']}")
        if result["message"]:
            print(f"   {result['message']}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

