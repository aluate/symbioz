"""Run DNS fix and show output"""

import subprocess
import sys

print("Running DNS fix script...")
print("=" * 70)

result = subprocess.run(
    [sys.executable, "fix_wedding_dns_complete.py"],
    cwd="e:\\My Drive",
    capture_output=True,
    text=True,
    timeout=60
)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

print("=" * 70)
print(f"Exit code: {result.returncode}")
