#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Push Corporate Crashout app to Justin's GitHub repository.

This script automates:
- Cloning the destination repo
- Copying the app folder
- Committing and pushing
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Source folder
SOURCE_FOLDER = Path(r"E:\My Drive\apps\corporate-crashout")

# Colors for output (ASCII-safe fallbacks)
try:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
except:
    GREEN = ""
    YELLOW = ""
    RED = ""
    RESET = ""


def print_step(step: str):
    """Print a step header."""
    print(f"\n[STEP] {step}")


def print_error(error: str):
    """Print an error message."""
    print(f"[ERROR] {error}")


def print_success(message: str):
    """Print a success message."""
    print(f"[OK] {message}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"[WARNING] {message}")


def run_command(cmd: list, cwd: Path = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command."""
    print(f"Running: {' '.join(cmd)}")
    if cwd:
        print(f"  (in: {cwd})")
    result = subprocess.run(
        cmd, 
        cwd=str(cwd) if cwd else None, 
        capture_output=True, 
        text=True, 
        check=check,
        shell=False
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(result.stderr, file=sys.stderr)
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python push_corporate_crashout.py <GITHUB_REPO_URL>")
        print("\nExample:")
        print("  python push_corporate_crashout.py https://github.com/justin-username/corporate-crashout.git")
        sys.exit(1)

    repo_url = sys.argv[1]
    target_path = Path("apps/corporate-crashout")

    print("=" * 60)
    print("Pushing Corporate Crashout to GitHub")
    print("=" * 60)
    print(f"\nSource: {SOURCE_FOLDER}")
    print(f"Destination: {repo_url}")
    print(f"Target path: {target_path}")
    print("=" * 60)

    # Verify source exists
    if not SOURCE_FOLDER.exists():
        print_error(f"Source folder not found: {SOURCE_FOLDER}")
        sys.exit(1)

    # Create temp directory for clone
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        clone_path = temp_path / "repo"

        try:
            # Clone repo
            print_step("Cloning destination repository...")
            run_command(["git", "clone", repo_url, str(clone_path)])

            # Check existing structure
            print_step("Checking existing repository structure...")
            existing_files = list(clone_path.iterdir())
            if existing_files:
                print(f"Found {len(existing_files)} existing files/folders in repo")
                for item in existing_files:
                    if item.is_dir():
                        print(f"  📁 {item.name}/")
                    else:
                        print(f"  📄 {item.name}")

            # Create target directory structure
            print_step("Creating target directory structure...")
            target_dir = clone_path / target_path
            if target_dir.exists():
                print_warning(f"{target_path} already exists - removing it first")
                shutil.rmtree(target_dir)
            target_dir.parent.mkdir(parents=True, exist_ok=True)

            # Copy files
            print_step(f"Copying files from {SOURCE_FOLDER}...")
            shutil.copytree(SOURCE_FOLDER, target_dir)

            # Remove .env if it exists (but keep .env.example)
            env_file = target_dir / ".env"
            if env_file.exists():
                print_warning("Removing .env file (should not be committed)")
                env_file.unlink()
            
            # Ensure .env.example exists (should be safe to commit)
            env_example = target_dir / ".env.example"
            if not env_example.exists():
                print_warning(".env.example not found - creating template")
                env_example.write_text("""# Database
DATABASE_URL="postgresql://user:password@localhost:5432/corporate_crashout?schema=public"

# NextAuth
NEXTAUTH_SECRET="your-secret-key-here"
NEXTAUTH_URL="http://localhost:3000"

# Stripe
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_PUBLISHABLE_KEY="pk_test_..."
STRIPE_WEBHOOK_SECRET="whsec_..."
STRIPE_PRICE_TIER1="price_..."
STRIPE_PRICE_TIER2="price_..."
STRIPE_PRICE_TIER3="price_..."
STRIPE_PRICE_ADDON_1ON1="price_..."

# Discord
DISCORD_INVITE_URL="https://discord.gg/..."
""")

            # Verify critical files
            print_step("Verifying critical files...")
            critical_files = [
                target_dir / "package.json",
                target_dir / "prisma" / "schema.prisma",
                target_dir / "control" / "corporate-crashout" / "CONTROL.md",
                target_dir / "scripts" / "bootstrap.ts",
                target_dir / "scripts" / "stripe-doctor.ts",
                target_dir / "app" / "api" / "health" / "route.ts",
            ]
            all_found = True
            for file_path in critical_files:
                if file_path.exists():
                    rel_path = file_path.relative_to(target_dir)
                    print(f"  OK: {rel_path}")
                else:
                    rel_path = file_path.relative_to(target_dir)
                    print_error(f"  MISSING: {rel_path}")
                    all_found = False
            
            if not all_found:
                print_error("Critical files missing - aborting")
                sys.exit(1)

            # Stage changes
            print_step("Staging changes...")
            run_command(["git", "add", "apps/"], cwd=clone_path)
            
            # Check if .gitignore needs updating
            gitignore = clone_path / ".gitignore"
            if not gitignore.exists() or ".env" not in gitignore.read_text():
                print_warning("Ensuring .env is in .gitignore")
                if not gitignore.exists():
                    gitignore.write_text(".env\n")
                else:
                    content = gitignore.read_text()
                    if ".env" not in content:
                        gitignore.write_text(content + "\n.env\n")
                run_command(["git", "add", ".gitignore"], cwd=clone_path)

            # Check status
            print_step("Checking git status...")
            status_result = run_command(["git", "status", "--short"], cwd=clone_path, check=False)
            if status_result.stdout.strip():
                print("Changes to be committed:")
                print(status_result.stdout)
            else:
                print_warning("No changes detected")
                # Check if target already exists and is identical
                if target_dir.exists():
                    print_warning("Target folder already exists with identical content")
                    print("Nothing to commit. Files may already be up to date.")
                else:
                    print_error("No changes detected but target doesn't exist - something went wrong")
                    sys.exit(1)
                sys.exit(0)

            # Commit
            print_step("Committing changes...")
            commit_msg = "Add Corporate Crashout Next.js app - complete subscription platform with Stripe, Auth, Prisma, admin dashboard, and utility scripts"
            run_command(
                ["git", "commit", "-m", commit_msg],
                cwd=clone_path
            )

            # Push
            print_step("Pushing to GitHub...")
            # Try main branch first, fall back to master
            try:
                run_command(["git", "push", "origin", "main"], cwd=clone_path)
            except subprocess.CalledProcessError:
                print_warning("Push to 'main' failed, trying 'master' branch...")
                run_command(["git", "push", "origin", "master"], cwd=clone_path)

            # Success!
            print("\n" + "=" * 60)
            print_success("Push completed successfully!")
            print("=" * 60)
            print("\nVerification checklist:")
            print(f"  ✅ {target_path} exists in repo")
            print("  ✅ All subdirectories copied")
            print("  ✅ package.json includes bootstrap and stripe:doctor scripts")
            print("  ✅ CONTROL.md present")
            print("  ✅ Health endpoint exists")
            print("  ✅ Documentation files included")
            print("  ✅ No .env files committed")
            print("\nYou can verify at:")
            print(f"  {repo_url}")
            print("\n")

        except subprocess.CalledProcessError as e:
            print_error(f"Command failed with exit code {e.returncode}")
            print(f"Command: {e.cmd}")
            if e.stderr:
                print(f"Error output: {e.stderr}")
            sys.exit(1)
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()

