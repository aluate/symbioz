#!/usr/bin/env python3
"""Run deployment and capture output to file."""

import os
import sys
import subprocess
from pathlib import Path

os.environ["VERCEL_TOKEN"] = "n6QnE86DsiIcQXIdQp0SA34P"
os.environ["CLOUDFLARE_API_TOKEN"] = "bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH"

script_path = Path(__file__).parent / "tools" / "deploy_corporate_crashout.py"
output_file = Path(__file__).parent / "DEPLOYMENT_RUN_OUTPUT.txt"

print(f"Running: {script_path}")
print(f"Output will be saved to: {output_file}")
print("="*70)

try:
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(Path(__file__).parent),
        capture_output=True,
        text=True,
        timeout=300,
        env=os.environ.copy()
    )
    
    output_lines = []
    output_lines.append("="*70)
    output_lines.append("DEPLOYMENT SCRIPT OUTPUT")
    output_lines.append("="*70)
    output_lines.append("")
    output_lines.append(result.stdout)
    
    if result.stderr:
        output_lines.append("")
        output_lines.append("STDERR:")
        output_lines.append("-"*70)
        output_lines.append(result.stderr)
    
    output_lines.append("")
    output_lines.append("="*70)
    output_lines.append(f"Exit Code: {result.returncode}")
    output_lines.append("="*70)
    
    output_text = "\n".join(output_lines)
    
    # Print to console
    print(output_text)
    
    # Write to file
    output_file.write_text(output_text, encoding='utf-8')
    print(f"\n✅ Full output saved to: {output_file}")
    
except subprocess.TimeoutExpired:
    print("❌ Script timed out after 5 minutes")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
