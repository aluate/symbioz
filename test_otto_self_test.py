#!/usr/bin/env python3
"""
Quick script to test Otto's self-test capability
This demonstrates Option B: Otto tests himself
"""

import requests
import json

OTTO_API = "http://localhost:8001"
LIFE_OS_API = "http://localhost:8000"

def test_otto_self_test():
    """Test Otto's self-test skill"""
    print("=" * 60)
    print("Testing Otto's Self-Test (Option B)")
    print("=" * 60)
    print()
    
    # Check if services are running
    print("Checking if services are running...")
    try:
        response = requests.get(f"{OTTO_API}/health", timeout=5)
        if response.status_code != 200:
            print(f"✗ Otto API not healthy (status {response.status_code})")
            return
        print("✓ Otto API is running")
    except Exception as e:
        print(f"✗ Cannot reach Otto API: {e}")
        print("\nPlease start services first:")
        print("  1. Run START_OTTO_WINDOWS.bat")
        print("  2. Run worker: python -m worker.otto_worker")
        return
    
    print()
    print("Asking Otto to test himself (quick test)...")
    print()
    
    # Test 1: Quick self-test (no DB writes)
    try:
        response = requests.post(
            f"{OTTO_API}/task",
            json={
                "type": "self_test",
                "payload": {
                    "test_type": "quick"
                },
                "source": "test_script"
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        print("Otto's Response:")
        print("-" * 60)
        print(result.get("message", "No message"))
        print("-" * 60)
        print()
        
        if result.get("status") == "success":
            print("✅ Quick self-test completed!")
            data = result.get("result", {})
            if data:
                print("\nTest Results:")
                if data.get("worker_test"):
                    worker = data["worker_test"]
                    status = "✓" if worker.get("ok") else "✗"
                    print(f"  {status} Worker: {worker.get('message', 'N/A')}")
                
                if data.get("api_test"):
                    api = data["api_test"]
                    status = "✓" if api.get("ok") else "✗"
                    print(f"  {status} APIs: {api.get('message', 'N/A')}")
                    if not api.get("ok") and api.get("issues"):
                        print(f"    Issues: {', '.join(api.get('issues', []))}")
        else:
            print(f"⚠ Self-test returned status: {result.get('status')}")
        
    except Exception as e:
        print(f"✗ Error running self-test: {e}")
        return
    
    print()
    print("=" * 60)
    print("Next: Try asking Otto via the Console!")
    print("=" * 60)
    print()
    print("1. Open http://localhost:3000/otto")
    print("2. Type: 'Run a self-test'")
    print("3. Or: 'Are you okay?'")
    print()
    print("For a full test (creates test task):")
    print("  Type: 'Run a full self-test'")
    print()

if __name__ == "__main__":
    try:
        test_otto_self_test()
    except KeyboardInterrupt:
        print("\n\nTest interrupted")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()

