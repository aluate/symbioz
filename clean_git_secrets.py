#!/usr/bin/env python3
"""
Clean secrets from git history using git filter-branch
"""

import subprocess
import sys
import re
from pathlib import Path

def clean_secrets_in_repo(repo_path: Path):
    """Clean secrets from git history"""
    
    # Files that contain secrets
    secret_files = [
        "QUICK_STRIPE_SETUP.md",
        "STRIPE_FINAL_STEPS.md",
        "DEPLOYMENT_DISCONNECT_ANALYSIS.md"
    ]
    
    # Create a tree-filter script that works in the git filter-branch context
    # The script needs to work from within the temporary checkout directory
    filter_script = '''import sys
import re
import os
from pathlib import Path

# Get current directory (where git filter-branch checks out files)
repo_root = Path(os.getcwd())

# Files to clean
files_to_clean = ["QUICK_STRIPE_SETUP.md", "STRIPE_FINAL_STEPS.md", "DEPLOYMENT_DISCONNECT_ANALYSIS.md"]

for filename in files_to_clean:
    filepath = repo_root / filename
    if filepath.exists():
        try:
            content = filepath.read_text(encoding='utf-8')
            original = content
            
            # Replace secrets
            content = re.sub(
                r'sk_test_51SZH87K3XMzVSHTY[a-zA-Z0-9]+',
                'sk_test_...REDACTED...',
                content
            )
            content = re.sub(
                r'ghp_[A-Za-z0-9]{36}',
                'ghp_...REDACTED...',
                content
            )
            content = re.sub(
                r'n6QnE86DsiIcQXIdQp0SA34P',
                'VERCEL_TOKEN_REDACTED',
                content
            )
            
            # Only write if changed
            if content != original:
                filepath.write_text(content, encoding='utf-8')
        except Exception:
            pass  # File might not exist in this commit or can't be read
'''
    
    # Write filter script to a temp location
    import tempfile
    temp_dir = Path(tempfile.gettempdir())
    filter_script_path = temp_dir / "git_filter_secrets.py"
    filter_script_path.write_text(filter_script, encoding='utf-8')
    
    # Use git filter-branch with tree-filter
    # Use absolute path to Python script
    tree_filter = f'python "{filter_script_path.absolute()}"'
    
    print("🔄 Cleaning secrets from git history...")
    print("   This may take a few minutes...")
    print()
    
    result = subprocess.run(
        ["git", "filter-branch", "--force", "--tree-filter", tree_filter,
         "--prune-empty", "--tag-name-filter", "cat", "--", "--all"],
        cwd=str(repo_path),
        capture_output=True,
        text=True,
        timeout=600
    )
    
    # Clean up script
    try:
        filter_script_path.unlink()
    except:
        pass
    
    if result.returncode == 0:
        print("✅ History cleaned successfully!")
        print()
        print("🧹 Cleaning up git references...")
        
        # Expire reflog
        subprocess.run(
            ["git", "reflog", "expire", "--expire=now", "--all"],
            cwd=str(repo_path),
            capture_output=True
        )
        
        # Garbage collect
        subprocess.run(
            ["git", "gc", "--prune=now", "--aggressive"],
            cwd=str(repo_path),
            capture_output=True
        )
        
        print("✅ Cleanup complete!")
        print()
        print("⚠️  IMPORTANT: You'll need to force push:")
        print("   git push --force origin main")
        print()
        return True
    else:
        print(f"❌ Failed: {result.stderr}")
        return False


if __name__ == "__main__":
    repo_path = Path("catered_by_me")
    if not repo_path.exists():
        print(f"❌ Repository not found: {repo_path}")
        sys.exit(1)
    
    success = clean_secrets_in_repo(repo_path)
    sys.exit(0 if success else 1)

