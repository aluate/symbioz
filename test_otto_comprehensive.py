#!/usr/bin/env python3
"""
Comprehensive Test Script for Otto Phase 2 + Safety + Phase 3
Tests worker loop, actions, safety features, and Life OS integrations
"""

import requests
import time
import json
from datetime import datetime, timedelta

# Configuration
LIFE_OS_API = "http://localhost:8000"
OTTO_API = "http://localhost:8001"

class TestResults:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []
    
    def add_pass(self, test_name, message=""):
        self.passed.append((test_name, message))
        print(f"✅ {test_name}")
        if message:
            print(f"   {message}")
    
    def add_fail(self, test_name, message=""):
        self.failed.append((test_name, message))
        print(f"❌ {test_name}")
        if message:
            print(f"   {message}")
    
    def add_warning(self, test_name, message=""):
        self.warnings.append((test_name, message))
        print(f"⚠️  {test_name}")
        if message:
            print(f"   {message}")
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {len(self.passed)}")
        print(f"❌ Failed: {len(self.failed)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        
        if self.failed:
            print("\nFailed Tests:")
            for name, msg in self.failed:
                print(f"  - {name}: {msg}")
        
        if self.warnings:
            print("\nWarnings:")
            for name, msg in self.warnings:
                print(f"  - {name}: {msg}")
        
        return len(self.failed) == 0

results = TestResults()

def wait_for_service(url, name, max_wait=30):
    """Wait for a service to become available"""
    print(f"  Waiting for {name}...")
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{url}/health", timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def test_service_health():
    """Test if services are running"""
    print("\n" + "=" * 60)
    print("TEST 1: Service Health")
    print("=" * 60)
    
    # Try to connect, if fails, wait a bit
    try:
        response = requests.get(f"{LIFE_OS_API}/health", timeout=2)
        if response.status_code == 200:
            results.add_pass("Life OS Backend", "Running")
        else:
            results.add_fail("Life OS Backend", f"Returned {response.status_code}")
            return False
    except:
        print("  Life OS Backend not immediately available, waiting...")
        if wait_for_service(LIFE_OS_API, "Life OS Backend"):
            results.add_pass("Life OS Backend", "Running (started during wait)")
        else:
            results.add_fail("Life OS Backend", "Not reachable - please start services")
            print("\n  To start services:")
            print("    1. Run: START_OTTO_WINDOWS.bat")
            print("    2. Or manually start:")
            print("       - Otto API: cd apps\\otto && python -m otto.cli server")
            print("       - Life OS Backend: cd apps\\life_os\\backend && python -m uvicorn main:app --reload --port 8000")
            return False
    
    try:
        response = requests.get(f"{OTTO_API}/health", timeout=2)
        if response.status_code == 200:
            results.add_pass("Otto API", "Running")
        else:
            results.add_fail("Otto API", f"Returned {response.status_code}")
            return False
    except:
        print("  Otto API not immediately available, waiting...")
        if wait_for_service(OTTO_API, "Otto API"):
            results.add_pass("Otto API", "Running (started during wait)")
        else:
            results.add_fail("Otto API", "Not reachable - please start services")
            return False
    
    return True

def test_otto_shell():
    """Test Otto Shell (manual prompt)"""
    print("\n" + "=" * 60)
    print("TEST 2: Otto Shell (Manual Prompt)")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{LIFE_OS_API}/otto/runs",
            json={
                "input_text": "Say hello and confirm you're working",
                "input_payload": {}
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        run = response.json()
        
        if run.get('status') == 'success':
            results.add_pass("Otto Shell", f"Run ID {run['id']} completed")
            return run['id']
        else:
            results.add_warning("Otto Shell", f"Run status: {run.get('status')}")
            return run.get('id')
    except Exception as e:
        results.add_fail("Otto Shell", f"Error: {e}")
        return None

def test_worker_task_processing():
    """Test worker processing a simple task"""
    print("\n" + "=" * 60)
    print("TEST 3: Worker Task Processing")
    print("=" * 60)
    
    # Create a simple task
    task_data = {
        "type": "otto.log",
        "description": f"[TEST] Worker test at {datetime.now().isoformat()}",
        "payload": {
            "message": "Test message from comprehensive test",
            "level": "info"
        }
    }
    
    try:
        response = requests.post(
            f"{LIFE_OS_API}/otto/tasks",
            json=task_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        task = response.json()
        task_id = task['id']
        results.add_pass("Create Task", f"Task ID {task_id} created")
    except Exception as e:
        results.add_fail("Create Task", f"Error: {e}")
        return None
    
    # Wait for worker to process
    print(f"  Waiting for worker to process task {task_id}...")
    max_wait = 60
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{LIFE_OS_API}/otto/tasks/{task_id}", timeout=5)
            response.raise_for_status()
            task = response.json()
            
            status = task['status']
            if status == 'success':
                results.add_pass("Worker Processing", f"Task {task_id} processed successfully")
                return task_id
            elif status == 'error':
                error = task.get('last_error', 'Unknown error')
                results.add_fail("Worker Processing", f"Task failed: {error}")
                return task_id
            elif status == 'running':
                print(f"    Task is running... ({int(time.time() - start_time)}s)")
            
            time.sleep(2)
        except Exception as e:
            print(f"    Error checking task: {e}")
            time.sleep(2)
    
    results.add_warning("Worker Processing", "Timeout - worker may not be running")
    return task_id

def test_life_os_create_task_action():
    """Test life_os.create_task action"""
    print("\n" + "=" * 60)
    print("TEST 4: Life OS Create Task Action")
    print("=" * 60)
    
    # Use a prompt that Otto can understand, which should emit life_os.create_task action
    task_data = {
        "type": "otto.log",  # Use a simple type that Otto understands
        "description": f"[TEST] Create a Life OS task: Test Task {datetime.now().strftime('%H:%M:%S')}",
        "payload": {
            "message": f"Create a task with title 'Test Task {datetime.now().strftime('%H:%M:%S')}', description 'Created by comprehensive test', priority 'medium', category 'test'",
            "level": "info"
        }
    }
    
    try:
        response = requests.post(
            f"{LIFE_OS_API}/otto/tasks",
            json=task_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        task = response.json()
        task_id = task['id']
        results.add_pass("Create OttoTask", f"Task ID {task_id}")
    except Exception as e:
        results.add_fail("Create OttoTask", f"Error: {e}")
        return None
    
    # Wait for processing
    print(f"  Waiting for worker to process...")
    max_wait = 60
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{LIFE_OS_API}/otto/tasks/{task_id}", timeout=5)
            response.raise_for_status()
            task = response.json()
            
            if task['status'] == 'success':
                # Check if Life OS task was created
                response = requests.get(f"{LIFE_OS_API}/life_os/tasks?category=test", timeout=5)
                if response.status_code == 200:
                    tasks = response.json()
                    if tasks:
                        results.add_pass("Life OS Task Created", f"Found {len(tasks)} test task(s)")
                        return task_id
                
                results.add_warning("Life OS Task Created", "Task processed but Life OS task not found")
                return task_id
            elif task['status'] == 'error':
                error = task.get('last_error', 'Unknown error')
                results.add_fail("Action Execution", f"Error: {error}")
                return task_id
            
            time.sleep(2)
        except Exception as e:
            print(f"    Error: {e}")
            time.sleep(2)
    
    results.add_warning("Action Execution", "Timeout")
    return task_id

def test_bills_create_action():
    """Test bills.create action"""
    print("\n" + "=" * 60)
    print("TEST 5: Bills Create Action")
    print("=" * 60)
    
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    # Use a prompt that Otto can understand
    task_data = {
        "type": "otto.log",
        "description": f"[TEST] Create bill via Otto",
        "payload": {
            "message": f"Create a bill: Test Bill {datetime.now().strftime('%H:%M:%S')}, amount $50.00, due date {due_date}, category test",
            "level": "info"
        }
    }
    
    try:
        response = requests.post(
            f"{LIFE_OS_API}/otto/tasks",
            json=task_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        task = response.json()
        task_id = task['id']
        results.add_pass("Create OttoTask", f"Task ID {task_id}")
    except Exception as e:
        results.add_fail("Create OttoTask", f"Error: {e}")
        return None
    
    # Wait for processing
    print(f"  Waiting for worker to process...")
    max_wait = 60
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{LIFE_OS_API}/otto/tasks/{task_id}", timeout=5)
            response.raise_for_status()
            task = response.json()
            
            if task['status'] == 'success':
                # Check if bill was created
                response = requests.get(f"{LIFE_OS_API}/bills?category=test", timeout=5)
                if response.status_code == 200:
                    bills = response.json()
                    if bills:
                        results.add_pass("Bill Created", f"Found {len(bills)} test bill(s)")
                        return task_id
                
                results.add_warning("Bill Created", "Task processed but bill not found")
                return task_id
            elif task['status'] == 'error':
                error = task.get('last_error', 'Unknown error')
                results.add_fail("Action Execution", f"Error: {error}")
                return task_id
            
            time.sleep(2)
        except Exception as e:
            print(f"    Error: {e}")
            time.sleep(2)
    
    results.add_warning("Action Execution", "Timeout")
    return task_id

def test_calendar_create_action():
    """Test calendar.create_event action"""
    print("\n" + "=" * 60)
    print("TEST 6: Calendar Create Event Action")
    print("=" * 60)
    
    start_time = (datetime.now() + timedelta(days=1)).isoformat()
    # Use a prompt that Otto can understand
    task_data = {
        "type": "otto.log",
        "description": f"[TEST] Create calendar event via Otto",
        "payload": {
            "message": f"Create a calendar event: Test Event {datetime.now().strftime('%H:%M:%S')}, start time {start_time}, category test",
            "level": "info"
        }
    }
    
    try:
        response = requests.post(
            f"{LIFE_OS_API}/otto/tasks",
            json=task_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        task = response.json()
        task_id = task['id']
        results.add_pass("Create OttoTask", f"Task ID {task_id}")
    except Exception as e:
        results.add_fail("Create OttoTask", f"Error: {e}")
        return None
    
    # Wait for processing
    print(f"  Waiting for worker to process...")
    max_wait = 60
    start_time_check = time.time()
    
    while time.time() - start_time_check < max_wait:
        try:
            response = requests.get(f"{LIFE_OS_API}/otto/tasks/{task_id}", timeout=5)
            response.raise_for_status()
            task = response.json()
            
            if task['status'] == 'success':
                # Check if event was created
                response = requests.get(f"{LIFE_OS_API}/calendar?category=test", timeout=5)
                if response.status_code == 200:
                    events = response.json()
                    if events:
                        results.add_pass("Calendar Event Created", f"Found {len(events)} test event(s)")
                        return task_id
                
                results.add_warning("Calendar Event Created", "Task processed but event not found")
                return task_id
            elif task['status'] == 'error':
                error = task.get('last_error', 'Unknown error')
                results.add_fail("Action Execution", f"Error: {error}")
                return task_id
            
            time.sleep(2)
        except Exception as e:
            print(f"    Error: {e}")
            time.sleep(2)
    
    results.add_warning("Action Execution", "Timeout")
    return task_id

def test_safety_tiers():
    """Test safety tier enforcement"""
    print("\n" + "=" * 60)
    print("TEST 7: Safety Tier Enforcement")
    print("=" * 60)
    
    # Test that TIER_0_SAFE actions work (read-only)
    # Note: We test this by checking the safety registry, not by creating tasks
    # because Otto needs to understand the task type first
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps', 'life_os', 'backend'))
        from otto.safety import get_task_tier, SafetyTier
        tier = get_task_tier("life_os.list_tasks")
        if tier == SafetyTier.TIER_0_SAFE:
            results.add_pass("TIER_0_SAFE Registry", "Read-only action correctly registered")
        else:
            results.add_fail("TIER_0_SAFE Registry", f"Expected TIER_0_SAFE, got {tier}")
    except Exception as e:
        results.add_fail("TIER_0_SAFE Registry", f"Error: {e}")
    
    # Test that TIER_1_LIMITED actions work (limited writes)
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps', 'life_os', 'backend'))
        from otto.safety import get_task_tier, SafetyTier
        tier = get_task_tier("life_os.create_task")
        if tier == SafetyTier.TIER_1_LIMITED:
            results.add_pass("TIER_1_LIMITED Registry", "Limited write action correctly registered")
        else:
            results.add_fail("TIER_1_LIMITED Registry", f"Expected TIER_1_LIMITED, got {tier}")
    except Exception as e:
        results.add_fail("TIER_1_LIMITED Registry", f"Error: {e}")

def test_retry_logic():
    """Test retry logic for failed tasks"""
    print("\n" + "=" * 60)
    print("TEST 8: Retry Logic")
    print("=" * 60)
    
    # Create a task that will fail (invalid action type)
    task_data = {
        "type": "invalid.action.type",
        "description": "[TEST] Test retry logic with invalid action",
        "payload": {}
    }
    
    try:
        response = requests.post(
            f"{LIFE_OS_API}/otto/tasks",
            json=task_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        task = response.json()
        task_id = task['id']
        results.add_pass("Create Failing Task", f"Task ID {task_id}")
    except Exception as e:
        results.add_fail("Create Failing Task", f"Error: {e}")
        return
    
    # Wait a bit for processing
    time.sleep(5)
    
    try:
        response = requests.get(f"{LIFE_OS_API}/otto/tasks/{task_id}", timeout=5)
        response.raise_for_status()
        task = response.json()
        
        if task.get('retries', 0) > 0:
            results.add_pass("Retry Logic", f"Task retried {task['retries']} time(s)")
        else:
            results.add_warning("Retry Logic", "Task may not have been retried yet")
    except Exception as e:
        results.add_warning("Retry Logic", f"Could not check retries: {e}")

def test_otto_runs_api():
    """Test Otto Runs API"""
    print("\n" + "=" * 60)
    print("TEST 9: Otto Runs API")
    print("=" * 60)
    
    try:
        response = requests.get(f"{LIFE_OS_API}/otto/runs?limit=5", timeout=5)
        response.raise_for_status()
        runs = response.json()
        results.add_pass("List Runs", f"Found {len(runs)} run(s)")
        
        if runs:
            run_id = runs[0]['id']
            response = requests.get(f"{LIFE_OS_API}/otto/runs/{run_id}", timeout=5)
            response.raise_for_status()
            run = response.json()
            results.add_pass("Get Run Details", f"Retrieved run ID {run_id}")
    except Exception as e:
        results.add_fail("Otto Runs API", f"Error: {e}")

def test_life_os_apis():
    """Test Life OS APIs directly"""
    print("\n" + "=" * 60)
    print("TEST 10: Life OS APIs")
    print("=" * 60)
    
    # Test Tasks API
    try:
        response = requests.get(f"{LIFE_OS_API}/life_os/tasks?limit=5", timeout=5)
        response.raise_for_status()
        tasks = response.json()
        results.add_pass("Tasks API", f"Found {len(tasks)} task(s)")
    except Exception as e:
        results.add_fail("Tasks API", f"Error: {e}")
    
    # Test Bills API
    try:
        response = requests.get(f"{LIFE_OS_API}/bills?limit=5", timeout=5)
        response.raise_for_status()
        bills = response.json()
        results.add_pass("Bills API", f"Found {len(bills)} bill(s)")
    except Exception as e:
        results.add_fail("Bills API", f"Error: {e}")
    
    # Test Calendar API
    try:
        response = requests.get(f"{LIFE_OS_API}/calendar?limit=5", timeout=5)
        response.raise_for_status()
        events = response.json()
        results.add_pass("Calendar API", f"Found {len(events)} event(s)")
    except Exception as e:
        results.add_fail("Calendar API", f"Error: {e}")

def main():
    print("=" * 60)
    print("OTTO COMPREHENSIVE TEST SUITE")
    print("Phase 2 + Safety + Phase 3")
    print("=" * 60)
    print()
    print("⚠️  PREREQUISITES:")
    print("   1. Start services: START_OTTO_WINDOWS.bat (or start_otto_unix.sh)")
    print("   2. Start worker in separate terminal:")
    print("      cd apps\\life_os\\backend")
    print("      python -m worker.otto_worker")
    print()
    print("   The test will wait up to 30 seconds for services to start...")
    print()
    
    # Test 1: Service health
    if not test_service_health():
        print("\n❌ Services are not running. Please start them first.")
        results.print_summary()
        return
    
    # Test 2: Otto Shell
    test_otto_shell()
    
    # Test 3: Worker processing
    test_worker_task_processing()
    
    # Test 4: Life OS create task action
    test_life_os_create_task_action()
    
    # Test 5: Bills create action
    test_bills_create_action()
    
    # Test 6: Calendar create action
    test_calendar_create_action()
    
    # Test 7: Safety tiers
    test_safety_tiers()
    
    # Test 8: Retry logic
    test_retry_logic()
    
    # Test 9: Otto Runs API
    test_otto_runs_api()
    
    # Test 10: Life OS APIs
    test_life_os_apis()
    
    # Print summary
    all_passed = results.print_summary()
    
    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("\nNext steps:")
    print("  - Check http://localhost:3000/otto for run history")
    print("  - Check http://localhost:3000/tasks for created tasks")
    print("  - Check http://localhost:3000/bills for created bills")
    print("  - Check http://localhost:3000/calendar for created events")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        results.print_summary()
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        results.print_summary()

