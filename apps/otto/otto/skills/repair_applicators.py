"""
Patch applicators for Vercel and Render deployment failures

Applies minimal fixes based on classified failure types.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


def apply_patch_vercel(category: str, classification: Dict[str, Any], repo_root: Path = None, dry_run: bool = False) -> Dict[str, Any]:
    """
    Apply patch for Vercel failure.
    
    Returns:
        {
            "success": bool,
            "files_changed": List[str],
            "message": str,
            "error": Optional[str]
        }
    """
    if repo_root is None:
        repo_root = Path.cwd()
    
    patch_info = classification.get("suggested_patch", {})
    files_changed = []
    
    try:
        if category == "next_command_not_found":
            # Fix: Update package.json to use npx next
            package_json_path = repo_root / "apps" / "symbioz-web" / "package.json"
            if package_json_path.exists():
                with open(package_json_path, "r") as f:
                    package_data = json.load(f)
                
                scripts = package_data.get("scripts", {})
                changed = False
                
                for script_name, script_cmd in scripts.items():
                    if isinstance(script_cmd, str) and script_cmd.startswith("next ") and "npx" not in script_cmd:
                        scripts[script_name] = script_cmd.replace("next ", "npx next ", 1)
                        changed = True
                
                if changed:
                    if dry_run:
                        # Show what would change
                        old_scripts = {k: v for k, v in scripts.items() if not (isinstance(v, str) and v.startswith("next ") and "npx" not in v)}
                        new_scripts = package_data.get("scripts", {})
                        diff_lines = []
                        for script_name, old_cmd in scripts.items():
                            new_cmd = new_scripts.get(script_name)
                            if old_cmd != new_cmd:
                                diff_lines.append(f"-   \"{script_name}\": \"{old_cmd}\"")
                                diff_lines.append(f"+   \"{script_name}\": \"{new_cmd}\"")
                        return {
                            "success": True,
                            "files_changed": [str(package_json_path)],
                            "message": "Would update package.json scripts to use 'npx next'",
                            "dry_run": True,
                            "diff": "\n".join(diff_lines)
                        }
                    else:
                        with open(package_json_path, "w") as f:
                            json.dump(package_data, f, indent=2)
                        files_changed.append(str(package_json_path))
                        return {
                            "success": True,
                            "files_changed": files_changed,
                            "message": "Updated package.json scripts to use 'npx next'"
                        }
            else:
                return {
                    "success": False,
                    "error": f"package.json not found at {package_json_path}"
                }
        
        elif category == "typescript_nullability":
            # Fix: Add null check (simple pattern only)
            file_path = repo_root / patch_info.get("file", "")
            if file_path.exists() and file_path.suffix in [".ts", ".tsx"]:
                line_num = patch_info.get("line", 0)
                if line_num > 0:
                    with open(file_path, "r") as f:
                        lines = f.readlines()
                    
                    if line_num <= len(lines):
                        # Try to add a simple null check before the problematic line
                        # This is a minimal fix - just add a guard if we can identify the pattern
                        target_line = lines[line_num - 1]
                        
                        # Look for common patterns like function calls with potentially null args
                        # This is conservative - only fix obvious cases
                        if "null" in target_line.lower() or "undefined" in target_line.lower():
                            # For now, just document the issue - actual fix requires more context
                            logger.warning(f"TypeScript nullability issue at {file_path}:{line_num} - requires manual review")
                            return {
                                "success": False,
                                "error": "TypeScript nullability fix requires more context. Manual review recommended."
                            }
                
                return {
                    "success": False,
                    "error": f"Could not locate line {line_num} in {file_path}"
                }
            else:
                return {
                    "success": False,
                    "error": f"File not found: {file_path}"
                }
        
        elif category in ["root_directory_missing_package", "missing_env_var", "install_command_issue"]:
            # These are config issues - create a note file
            note_file = repo_root / "docs" / "deploy_failures_latest.md"
            note_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(note_file, "w") as f:
                f.write(f"# Deployment Failure - {category}\n\n")
                f.write(f"**Classification:** {category}\n")
                f.write(f"**Confidence:** {classification.get('confidence', 0)}\n\n")
                f.write(f"**Recommended Action:**\n")
                f.write(f"{patch_info.get('message', 'Manual review required')}\n\n")
                f.write(f"**Key Errors:**\n")
                for error in classification.get("key_errors", [])[:5]:
                    f.write(f"- {error}\n")
            
            files_changed.append(str(note_file))
            return {
                "success": True,
                "files_changed": files_changed,
                "message": f"Created failure diagnosis document"
            }
        
        else:
            return {
                "success": False,
                "error": f"Unsupported category: {category}"
            }
    
    except Exception as e:
        logger.error(f"Error applying Vercel patch: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def apply_patch_render(category: str, classification: Dict[str, Any], repo_root: Path = None, dry_run: bool = False) -> Dict[str, Any]:
    """
    Apply patch for Render failure.
    
    Returns:
        {
            "success": bool,
            "files_changed": List[str],
            "message": str,
            "error": Optional[str]
        }
    """
    if repo_root is None:
        repo_root = Path.cwd()
    
    patch_info = classification.get("suggested_patch", {})
    files_changed = []
    
    try:
        if category == "docker_copy_path":
            # Fix: Correct Dockerfile COPY paths for Render build context
            # CRITICAL: Must respect RENDER_ROOT_DIR setting
            # If Root Directory = apps/otto, build context IS apps/otto, so paths should NOT have apps/otto/ prefix
            # If Root Directory = . (repo root), then paths need apps/otto/ prefix
            
            render_root_dir = os.getenv("RENDER_ROOT_DIR", "apps/otto")  # Default to apps/otto
            dockerfile_path = repo_root / "apps" / "otto" / "Dockerfile"
            
            if dockerfile_path.exists():
                with open(dockerfile_path, "r") as f:
                    lines = f.readlines()
                
                modified = False
                new_lines = []
                
                for line in lines:
                    # Check if this is a COPY command
                    if line.strip().upper().startswith("COPY"):
                        # Extract the source path
                        copy_match = re.match(r"COPY\s+([^\s]+)\s+", line, re.IGNORECASE)
                        if copy_match:
                            source_path = copy_match.group(1)
                            
                            # Check if path exists relative to Dockerfile location (apps/otto/)
                            dockerfile_dir = dockerfile_path.parent
                            test_path = dockerfile_dir / source_path
                            
                            # Determine correct path based on Render root directory
                            if render_root_dir == "apps/otto" or render_root_dir.endswith("/otto"):
                                # Build context is apps/otto, so paths should be relative to apps/otto (no prefix)
                                # If path has apps/otto/ prefix, REMOVE it
                                if source_path.startswith("apps/otto/"):
                                    new_source = source_path.replace("apps/otto/", "", 1)
                                    line = line.replace(f"COPY {source_path}", f"COPY {new_source}", 1)
                                    modified = True
                                    logger.info(f"Fixed COPY path for root_dir={render_root_dir}: {source_path} -> {new_source}")
                                elif not test_path.exists():
                                    # Path doesn't exist - might need to check if it's a valid relative path
                                    # For apps/otto root, valid paths are: requirements.txt, otto/, otto_config.yaml
                                    if source_path not in ["requirements.txt", "otto/", "otto_config.yaml"] and not source_path.startswith("otto/"):
                                        logger.warning(f"COPY path {source_path} may be incorrect for root_dir={render_root_dir}")
                            else:
                                # Build context is repo root, so paths need apps/otto/ prefix
                                if not source_path.startswith("apps/otto/") and not test_path.exists():
                                    # Try to fix: if requirements.txt, otto/, or otto_config.yaml
                                    if source_path == "requirements.txt":
                                        new_source = "apps/otto/requirements.txt"
                                        line = line.replace(f"COPY {source_path}", f"COPY {new_source}", 1)
                                        modified = True
                                        logger.info(f"Fixed COPY path for root_dir={render_root_dir}: {source_path} -> {new_source}")
                                    elif source_path.startswith("otto/"):
                                        new_source = f"apps/otto/{source_path}"
                                        line = line.replace(f"COPY {source_path}", f"COPY {new_source}", 1)
                                        modified = True
                                        logger.info(f"Fixed COPY path for root_dir={render_root_dir}: {source_path} -> {new_source}")
                                    elif source_path == "otto_config.yaml":
                                        new_source = "apps/otto/otto_config.yaml"
                                        line = line.replace(f"COPY {source_path}", f"COPY {new_source}", 1)
                                        modified = True
                                        logger.info(f"Fixed COPY path for root_dir={render_root_dir}: {source_path} -> {new_source}")
                    
                    new_lines.append(line)
                
                if modified:
                    if dry_run:
                        # In dry-run, show what would change
                        diff_lines = []
                        for old_line, new_line in zip(lines, new_lines):
                            if old_line != new_line:
                                diff_lines.append(f"- {old_line.rstrip()}")
                                diff_lines.append(f"+ {new_line.rstrip()}")
                        return {
                            "success": True,
                            "files_changed": [str(dockerfile_path)],
                            "message": "Would fix Dockerfile COPY paths for Render build context",
                            "dry_run": True,
                            "diff": "\n".join(diff_lines)
                        }
                    else:
                        with open(dockerfile_path, "w") as f:
                            f.writelines(new_lines)
                        files_changed.append(str(dockerfile_path))
                        return {
                            "success": True,
                            "files_changed": files_changed,
                            "message": f"Fixed Dockerfile COPY paths for Render build context (root_dir={render_root_dir})"
                        }
                else:
                    # Paths look correct, but still failing - might be build context issue
                    # Create a note about checking Render build context setting
                    note_file = repo_root / "docs" / "deploy_failures_latest.md"
                    note_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(note_file, "w") as f:
                        f.write(f"# Render Deployment Failure - {category}\n\n")
                        f.write(f"**Classification:** {category}\n")
                        f.write(f"**Confidence:** {classification.get('confidence', 0)}\n\n")
                        f.write(f"**Issue:** Dockerfile COPY paths may be correct, but Render build context may be wrong.\n\n")
                        f.write(f"**Recommended Action:**\n")
                        f.write(f"1. Verify Render service Root Directory is set to 'apps/otto'\n")
                        f.write(f"2. If Root Directory is repo root, COPY paths need 'apps/otto/' prefix\n")
                        f.write(f"3. Check Render service settings → Root Directory\n\n")
                        f.write(f"**Key Errors:**\n")
                        for error in classification.get("key_errors", [])[:5]:
                            f.write(f"- {error}\n")
                    
                    files_changed.append(str(note_file))
                    return {
                        "success": True,
                        "files_changed": files_changed,
                        "message": "Created Dockerfile context diagnosis (paths appear correct)"
                    }
            else:
                return {
                    "success": False,
                    "error": f"Dockerfile not found at {dockerfile_path}"
                }
        
        elif category == "port_binding":
            # Fix: Ensure Dockerfile CMD uses $PORT env var
            dockerfile_path = repo_root / "apps" / "otto" / "Dockerfile"
            if dockerfile_path.exists():
                with open(dockerfile_path, "r") as f:
                    lines = f.readlines()
                
                modified = False
                new_lines = []
                in_cmd = False
                
                for i, line in enumerate(lines):
                    # Check CMD line
                    if line.strip().upper().startswith("CMD"):
                        in_cmd = True
                        # Check if it uses PORT env var
                        if "$PORT" not in line and "os.getenv('PORT'" not in line:
                            # Fix: Replace hardcoded port with PORT env var
                            # Look for patterns like port=8001 or port 8001
                            port_pattern = r"port[=\s]+(\d+)"
                            match = re.search(port_pattern, line, re.IGNORECASE)
                            if match:
                                # Replace with PORT env var pattern
                                old_port = match.group(1)
                                # Use Python pattern that's already in the Dockerfile
                                new_cmd = 'CMD python -c "import os; port = int(os.getenv(\'PORT\', 8001)); import uvicorn; uvicorn.run(\'otto.api:app\', host=\'0.0.0.0\', port=port)"\n'
                                line = new_cmd
                                modified = True
                                logger.info(f"Fixed CMD to use PORT env var")
                        new_lines.append(line)
                    elif in_cmd and line.strip().startswith("#"):
                        # Comment after CMD, keep it
                        new_lines.append(line)
                        in_cmd = False
                    else:
                        new_lines.append(line)
                        in_cmd = False
                
                if modified:
                    if dry_run:
                        diff_lines = []
                        for old_line, new_line in zip(lines, new_lines):
                            if old_line != new_line:
                                diff_lines.append(f"- {old_line.rstrip()}")
                                diff_lines.append(f"+ {new_line.rstrip()}")
                        return {
                            "success": True,
                            "files_changed": [str(dockerfile_path)],
                            "message": "Would fix Dockerfile to use PORT environment variable",
                            "dry_run": True,
                            "diff": "\n".join(diff_lines)
                        }
                    else:
                        with open(dockerfile_path, "w") as f:
                            f.writelines(new_lines)
                        files_changed.append(str(dockerfile_path))
                        return {
                            "success": True,
                            "files_changed": files_changed,
                            "message": "Fixed Dockerfile to use PORT environment variable"
                        }
                else:
                    # Already correct
                    return {
                        "success": True,
                        "files_changed": [],
                        "message": "Dockerfile already uses PORT env var correctly"
                    }
            else:
                return {
                    "success": False,
                    "error": f"Dockerfile not found at {dockerfile_path}"
                }
        
        elif category == "missing_python_module":
            # Fix: Add missing package to requirements.txt
            requirements_path = repo_root / "apps" / "otto" / "requirements.txt"
            package_name = patch_info.get("package", "")
            
            if not package_name:
                # Try to extract from key_errors
                key_errors = classification.get("key_errors", [])
                for error in key_errors:
                    module_match = re.search(r"no module named ['\"](.+?)['\"]", error.lower())
                    if module_match:
                        package_name = module_match.group(1)
                        break
            
            if requirements_path.exists() and package_name:
                with open(requirements_path, "r") as f:
                    requirements = f.read()
                    existing_packages = [line.strip().split(">=")[0].split("==")[0].split("[")[0].strip() 
                                       for line in requirements.split("\n") if line.strip() and not line.strip().startswith("#")]
                
                # Normalize package name (handle cases like 'requests' vs 'Requests')
                package_lower = package_name.lower().strip()
                package_normalized = package_name.strip()
                
                # Check if package is already there (case-insensitive)
                if not any(pkg.lower() == package_lower for pkg in existing_packages):
                    # Map common module names to package names
                    package_mapping = {
                        "yaml": "pyyaml",
                        "dotenv": "python-dotenv",
                        "pydantic_settings": "pydantic-settings",
                    }
                    
                    install_name = package_mapping.get(package_lower, package_normalized)
                    
                    if dry_run:
                        return {
                            "success": True,
                            "files_changed": [str(requirements_path)],
                            "message": f"Would add {install_name} to requirements.txt (module: {package_name})",
                            "dry_run": True,
                            "diff": f"+ {install_name}\n"
                        }
                    else:
                        # Add package (add at end, with newline)
                        with open(requirements_path, "a") as f:
                            if not requirements.endswith("\n"):
                                f.write("\n")
                            f.write(f"{install_name}\n")
                        
                        files_changed.append(str(requirements_path))
                        return {
                            "success": True,
                            "files_changed": files_changed,
                            "message": f"Added {install_name} to requirements.txt (module: {package_name})"
                        }
                else:
                    return {
                        "success": True,
                        "files_changed": [],
                        "message": f"Package {package_name} already in requirements.txt"
                    }
            else:
                return {
                    "success": False,
                    "error": f"requirements.txt not found at {requirements_path} or could not extract package name"
                }
        
        elif category == "docker_workdir":
            # Fix: Ensure WORKDIR is set correctly
            dockerfile_path = repo_root / "apps" / "otto" / "Dockerfile"
            if dockerfile_path.exists():
                with open(dockerfile_path, "r") as f:
                    lines = f.readlines()
                
                modified = False
                new_lines = []
                has_workdir = False
                
                for i, line in enumerate(lines):
                    if line.strip().upper().startswith("WORKDIR"):
                        has_workdir = True
                        # Verify WORKDIR is /app (standard)
                        if "/app" not in line:
                            line = "WORKDIR /app\n"
                            modified = True
                            logger.info("Fixed WORKDIR to /app")
                        new_lines.append(line)
                    else:
                        new_lines.append(line)
                
                # If no WORKDIR found, add it after FROM
                if not has_workdir:
                    for i, line in enumerate(new_lines):
                        if line.strip().upper().startswith("FROM"):
                            # Insert WORKDIR after FROM
                            new_lines.insert(i + 1, "WORKDIR /app\n")
                            modified = True
                            logger.info("Added missing WORKDIR /app")
                            break
                
                if modified:
                    if dry_run:
                        diff_lines = []
                        for old_line, new_line in zip(lines, new_lines):
                            if old_line != new_line:
                                diff_lines.append(f"- {old_line.rstrip()}")
                                diff_lines.append(f"+ {new_line.rstrip()}")
                        return {
                            "success": True,
                            "files_changed": [str(dockerfile_path)],
                            "message": "Would fix Dockerfile WORKDIR",
                            "dry_run": True,
                            "diff": "\n".join(diff_lines)
                        }
                    else:
                        with open(dockerfile_path, "w") as f:
                            f.writelines(new_lines)
                        files_changed.append(str(dockerfile_path))
                        return {
                            "success": True,
                            "files_changed": files_changed,
                            "message": "Fixed Dockerfile WORKDIR"
                        }
                else:
                    return {
                        "success": True,
                        "files_changed": [],
                        "message": "WORKDIR already correct"
                    }
            else:
                return {
                    "success": False,
                    "error": f"Dockerfile not found at {dockerfile_path}"
                }
        
        elif category == "render_python_root_dir":
            # Render is using Python runtime but Root Directory is not set
            # This requires Render dashboard configuration - create diagnosis note
            note_file = repo_root / "docs" / "deploy_failures_latest.md"
            note_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(note_file, "w") as f:
                f.write(f"# Render Deployment Failure - {category}\n\n")
                f.write(f"**Classification:** {category}\n")
                f.write(f"**Confidence:** {classification.get('confidence', 0)}\n\n")
                f.write(f"**Issue:** Render is using Python runtime but cannot find `requirements.txt`.\n")
                f.write(f"This means Root Directory is not set to `apps/otto`.\n\n")
                f.write(f"**Recommended Action (Choose One):**\n\n")
                f.write(f"### Option 1: Use Docker Runtime (RECOMMENDED)\n")
                f.write(f"1. Go to Render Dashboard → Your Service → Settings\n")
                f.write(f"2. Change Runtime from 'Python' to 'Docker'\n")
                f.write(f"3. Verify Root Directory is set to `apps/otto`\n")
                f.write(f"4. Save - Render will automatically redeploy\n\n")
                f.write(f"### Option 2: Fix Python Runtime\n")
                f.write(f"1. Go to Render Dashboard → Your Service → Settings\n")
                f.write(f"2. Set Root Directory to `apps/otto`\n")
                f.write(f"3. Verify Build Command: `pip install -r requirements.txt`\n")
                f.write(f"4. Verify Start Command: `python -m uvicorn otto.api:app --host 0.0.0.0 --port $PORT`\n")
                f.write(f"5. Save - Render will automatically redeploy\n\n")
                f.write(f"**See:** `docs/otto_render_fix_requirements_txt_error.md` for detailed steps\n\n")
                f.write(f"**Key Errors:**\n")
                for error in classification.get("key_errors", [])[:5]:
                    f.write(f"- {error}\n")
            
            files_changed.append(str(note_file))
            return {
                "success": True,
                "files_changed": files_changed,
                "message": "Created Root Directory diagnosis (requires Render dashboard config - see docs/otto_render_fix_requirements_txt_error.md)"
            }
        
        elif category == "python_import_path":
            # This requires code analysis - create diagnosis note
            note_file = repo_root / "docs" / "deploy_failures_latest.md"
            note_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(note_file, "w") as f:
                f.write(f"# Render Deployment Failure - {category}\n\n")
                f.write(f"**Classification:** {category}\n")
                f.write(f"**Confidence:** {classification.get('confidence', 0)}\n\n")
                f.write(f"**Recommended Action:**\n")
                f.write(f"{patch_info.get('message', 'Check Python import paths match package structure')}\n\n")
                f.write(f"**Key Errors:**\n")
                for error in classification.get("key_errors", [])[:10]:
                    f.write(f"- {error}\n")
            
            files_changed.append(str(note_file))
            return {
                "success": True,
                "files_changed": files_changed,
                "message": f"Created failure diagnosis document (requires code analysis)"
            }
        
        else:
            return {
                "success": False,
                "error": f"Unsupported category: {category}"
            }
    
    except Exception as e:
        logger.error(f"Error applying Render patch: {e}")
        return {
            "success": False,
            "error": str(e)
        }

