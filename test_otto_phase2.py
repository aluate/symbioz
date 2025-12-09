#!/usr/bin/env python3
"""
Test script for Phase 2 - Otto Worker and Actions
Run this to verify everything is working
"""

import requests
import time
import json
from datetime import datetime

# Configuration
LIFE_OS_API = "http://localhost:8000"
OTTO_API = "http://localhost:8001"

def test_service_health():
    """Test if services are running"""
    print("Testing service health...")
    
    try:
        response = requests.get(f"{LIFE_OS_API}/health", timeout=5)
        if response.status_code == 200:
            print("✓ Life OS Backend is running")
        else:
            print(f"✗ Life OS Backend returned {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Life OS Backend not reachable: {e}")
        return False
    
    try:
        response = requests.get(f"{OTTO_API}/health", timeout=5)
        if response.status_code == 200:
            print("✓ Otto API is running")
        else:
            print(f"✗ Otto API returned {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Otto API not reachable: {e}")
        return False
    
    return True

def create_test_task():
    """Create a simple test task"""
    print("\nCreating test task...")
    
    task_data = {
        "type": "otto.log",
        "description": f"Test task created at {datetime.now().isoformat()}",
        "payload": {
            "message": "Hello from Phase 2 test!",
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
        print(f"✓ Task created: ID {task['id']}")
        return task['id']
    except Exception as e:
        print(f"✗ Failed to create task: {e}")
        return None

def wait_for_task_processing(task_id, max_wait=60):
    """Wait for task to be processed by worker"""
    print(f"\nWaiting for task {task_id} to be processed (max {max_wait}s)...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{LIFE_OS_API}/otto/tasks/{task_id}", timeout=5)
            response.raise_for_status()
            task = response.json()
            
            status = task['status']
            print(f"  Task status: {status}")
            
            if status in ['success', 'error']:
                return task
            elif status == 'running':
                print("  Task is being processed...")
            
            time.sleep(2)
        except Exception as e:
            print(f"  Error checking task: {e}")
            time.sleep(2)
    
    print("  ⚠ Timeout waiting for task to complete")
    return None

def check_run_created(task_id):
    """Check if an OttoRun was created for this task"""
    print(f"\nChecking for OttoRun created from task {task_id}...")
    
    try:
        response = requests.get(f"{LIFE_OS_API}/otto/runs?limit=10", timeout=5)
        response.raise_for_status()
        runs = response.json()
        
        # Look for a run with source="worker" that references this task
        for run in runs:
            if run.get('source') == 'worker':
                payload = run.get('input_payload', {})
                if payload.get('task_id') == task_id:
                    print(f"✓ Found OttoRun ID {run['id']} for task {task_id}")
                    print(f"  Status: {run['status']}")
                    print(f"  Output: {run.get('output_text', 'N/A')[:100]}...")
                    return run
        
        print("  ⚠ No worker run found for this task yet")
        return None
    except Exception as e:
        print(f"✗ Error checking runs: {e}")
        return None

def main():
    print("=" * 60)
    print("Otto Phase 2 Test Script")
    print("=" * 60)
    print()
    
    # Test 1: Service health
    if not test_service_health():
        print("\n❌ Services are not running. Please start them first:")
        print("  - Run START_OTTO_WINDOWS.bat (or start_otto_unix.sh)")
        print("  - Run worker: python -m worker.otto_worker")
        return
    
    # Test 2: Create task
    task_id = create_test_task()
    if not task_id:
        print("\n❌ Failed to create test task")
        return
    
    # Test 3: Wait for processing
    print("\n⚠ NOTE: Make sure the worker is running!")
    print("  If worker is not running, task will remain 'pending'")
    print()
    
    processed_task = wait_for_task_processing(task_id)
    
    if processed_task:
        if processed_task['status'] == 'success':
            print("\n✓ Task processed successfully!")
        else:
            print(f"\n⚠ Task completed with status: {processed_task['status']}")
            if processed_task.get('last_error'):
                print(f"  Error: {processed_task['last_error']}")
    else:
        print("\n⚠ Task may still be pending (worker might not be running)")
    
    # Test 4: Check for run
    run = check_run_created(task_id)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    if processed_task and processed_task['status'] == 'success' and run:
        print("✅ All tests passed! Phase 2 is working correctly.")
        print("\nNext steps:")
        print("  1. Open http://localhost:3000/otto to see the run")
        print("  2. Try creating more complex tasks")
        print("  3. Check the worker console for processing logs")
    else:
        print("⚠ Some tests had issues. Check:")
        print("  - Are all services running?")
        print("  - Is the worker running?")
        print("  - Check service logs for errors")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()

