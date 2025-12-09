#!/usr/bin/env python3
"""
Otto task: Fix wedding site build errors and deploy
"""

import subprocess
import json
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def check_build_errors():
    """Check for common build errors in wedding site"""
    repo_root = Path(__file__).parent
    wedding_dir = repo_root / "apps" / "wedding"
    
    errors = []
    
    # Check if node_modules exists
    if not (wedding_dir / "node_modules").exists():
        errors.append("Missing node_modules - need to run npm install")
    
    # Check for TypeScript errors
    print("Checking TypeScript configuration...")
    tsconfig = wedding_dir / "tsconfig.json"
    if not tsconfig.exists():
        errors.append("Missing tsconfig.json")
    
    # Check for missing config file
    config_file = wedding_dir / "config" / "wedding_config.json"
    if not config_file.exists():
        errors.append("Missing wedding_config.json")
    
    # Check package.json
    package_json = wedding_dir / "package.json"
    if not package_json.exists():
        errors.append("Missing package.json")
    
    return errors

def fix_common_issues():
    """Fix common build issues"""
    repo_root = Path(__file__).parent
    wedding_dir = repo_root / "apps" / "wedding"
    
    fixes = []
    
    # Ensure node_modules exists
    if not (wedding_dir / "node_modules").exists():
        print("Installing dependencies...")
        code, out, err = run_command("npm install", cwd=wedding_dir)
        if code == 0:
            fixes.append("Installed npm dependencies")
        else:
            fixes.append(f"Failed to install dependencies: {err}")
    
    # Check for missing imports or type errors
    # This would need actual build output to diagnose
    
    return fixes

def main():
    print("=" * 60)
    print("Otto: Fixing Wedding Site Build")
    print("=" * 60)
    
    errors = check_build_errors()
    if errors:
        print("\nFound issues:")
        for error in errors:
            print(f"  - {error}")
    
    fixes = fix_common_issues()
    if fixes:
        print("\nApplied fixes:")
        for fix in fixes:
            print(f"  - {fix}")
    
    print("\nNext: Check Vercel build logs for specific errors")
    return 0

if __name__ == "__main__":
    sys.exit(main())

