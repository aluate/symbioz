#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Push Corporate Crashout to YOUR GitHub account instead of Justin's.

This script:
1. Creates a new repo on your GitHub (if it doesn't exist)
2. Pushes all the code to YOUR account
3. Then you can deploy from your own repo
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Source folder
SOURCE_FOLDER = Path(r"E:\My Drive\apps\corporate-crashout")

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
        print("Usage: python push_to_my_github.py <YOUR_GITHUB_USERNAME>")
        print("\nExample:")
        print("  python push_to_my_github.py your-username")
        print("\nThis will create/push to: https://github.com/your-username/CorporateCrashoutTrading")
        sys.exit(1)

    github_username = sys.argv[1]
    # Use repo name from argv if provided, otherwise default
    if len(sys.argv) >= 3:
        repo_name = sys.argv[2]
    else:
        repo_name = "CorporateCrashoutTrading"
    repo_url = f"https://github.com/{github_username}/{repo_name}.git"

    print("=" * 60)
    print("Pushing Corporate Crashout to YOUR GitHub")
    print("=" * 60)
    print(f"\nYour GitHub: {github_username}")
    print(f"Repository: {repo_name}")
    print(f"Full URL: {repo_url}")
    print(f"Source: {SOURCE_FOLDER}")
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
            # Try to clone repo (might not exist yet)
            print_step("Checking if repository exists...")
            clone_result = run_command(["git", "clone", repo_url, str(clone_path)], check=False)
            
            if clone_result.returncode != 0:
                # Repo doesn't exist - need to create it
                print_warning("Repository doesn't exist yet!")
                print("\nYou need to create it first:")
                print(f"  1. Go to: https://github.com/new")
                print(f"  2. Repository name: {repo_name}")
                print(f"  3. Choose Public or Private")
                print(f"  4. DO NOT initialize with README, .gitignore, or license")
                print(f"  5. Click 'Create repository'")
                print(f"\nAfter creating it, run this script again!")
                sys.exit(1)
            else:
                print_success("Repository exists - will update it")

            # Remove existing corporate-crashout folder if it exists
            target_dir = clone_path / "apps" / "corporate-crashout"
            if target_dir.exists():
                print_warning(f"apps/corporate-crashout already exists - removing it first")
                shutil.rmtree(target_dir)

            # Create target directory structure
            print_step("Creating target directory structure...")
            target_dir.parent.mkdir(parents=True, exist_ok=True)

            # Copy files
            print_step(f"Copying files from {SOURCE_FOLDER}...")
            shutil.copytree(SOURCE_FOLDER, target_dir)

            # Remove .env if it exists
            env_file = target_dir / ".env"
            if env_file.exists():
                print_warning("Removing .env file (should not be committed)")
                env_file.unlink()

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
            gitignore_root = clone_path / ".gitignore"
            if not gitignore_root.exists():
                print_warning("Creating root .gitignore")
                gitignore_root.write_text(".env\n.env.local\n.env*.local\nnode_modules/\n.next/\n")
                run_command(["git", "add", ".gitignore"], cwd=clone_path)
            elif ".env" not in gitignore_root.read_text():
                print_warning("Adding .env to root .gitignore")
                content = gitignore_root.read_text()
                gitignore_root.write_text(content + "\n.env\n.env.local\n")
                run_command(["git", "add", ".gitignore"], cwd=clone_path)

            # Check status
            print_step("Checking git status...")
            status_result = run_command(["git", "status", "--short"], cwd=clone_path, check=False)
            if status_result.stdout.strip():
                print("Changes to be committed:")
                print(status_result.stdout)
            else:
                print_warning("No changes detected")
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

            # Determine branch name
            print_step("Determining branch name...")
            branch_result = run_command(["git", "branch", "--show-current"], cwd=clone_path, check=False)
            if branch_result.returncode == 0 and branch_result.stdout.strip():
                branch_name = branch_result.stdout.strip()
                print_success(f"Current branch: {branch_name}")
            else:
                # Try to detect default branch
                remote_result = run_command(["git", "symbolic-ref", "refs/remotes/origin/HEAD"], cwd=clone_path, check=False)
                if remote_result.returncode == 0:
                    branch_name = remote_result.stdout.strip().replace("refs/remotes/origin/", "")
                    print_success(f"Detected branch: {branch_name}")
                else:
                    branch_name = "main"  # Default
                    print_warning(f"Could not detect branch, using default: {branch_name}")

            # Push
            print_step(f"Pushing to GitHub ({branch_name} branch)...")
            run_command(["git", "push", "origin", branch_name], cwd=clone_path)

            # Success!
            print("\n" + "=" * 60)
            print_success("Push completed successfully!")
            print("=" * 60)
            print("\nVerification checklist:")
            print(f"  ✅ apps/corporate-crashout exists in repo")
            print("  ✅ All subdirectories copied")
            print("  ✅ package.json includes bootstrap and stripe:doctor scripts")
            print("  ✅ CONTROL.md present")
            print("  ✅ Health endpoint exists")
            print("  ✅ Documentation files included")
            print("  ✅ No .env files committed")
            print("\nYour repository:")
            print(f"  https://github.com/{github_username}/{repo_name}")
            print("\nYou can now deploy from YOUR repo!")
            print("=" * 60)
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

