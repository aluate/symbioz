#!/usr/bin/env python3
"""Run deployment and show output."""

import os
import sys
import subprocess
from pathlib import Path

os.environ["VERCEL_TOKEN"] = "n6QnE86DsiIcQXIdQp0SA34P"
os.environ["CLOUDFLARE_API_TOKEN"] = "bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH"

script_path = Path(__file__).parent / "tools" / "deploy_corporate_crashout.py"

print("="*70)
print("RUNNING DEPLOYMENT SCRIPT")
print("="*70)
print(f"Script: {script_path}")
print("="*70)
print()

try:
    # Force UTF-8 output
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(Path(__file__).parent),
        env=os.environ.copy(),
        timeout=300,
        text=True,
        bufsize=1,
        encoding='utf-8',
        errors='replace'
    )
    
    print()
    print("="*70)
    print(f"Script completed with exit code: {result.returncode}")
    print("="*70)
    
    if result.stdout:
        print("\nSTDOUT:")
        print("-"*70)
        print(result.stdout)
    
    if result.stderr:
        print("\nSTDERR:")
        print("-"*70)
        print(result.stderr)
        
except subprocess.TimeoutExpired:
    print("❌ Script timed out after 5 minutes")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
