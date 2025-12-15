"""
Failure classifiers for Vercel and Render deployments

Classifies common failure patterns and suggests fixes with confidence scores.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


def parse_vercel_failure(log_text: str, logs: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Parse Vercel build failure and classify it.
    
    Returns:
        {
            "category": str,
            "confidence": float (0.0-1.0),
            "suggested_patch": Dict with fix details,
            "key_errors": List[str]
        }
    """
    log_lower = log_text.lower()
    key_errors = []
    
    # Extract key error lines
    error_patterns = [
        r"error[:\s]+(.+)",
        r"failed[:\s]+(.+)",
        r"cannot find[:\s]+(.+)",
        r"module not found[:\s]+(.+)",
        r"cannot resolve[:\s]+(.+)",
    ]
    
    for line in log_text.split("\n"):
        for pattern in error_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                key_errors.append(line.strip())
                break
    
    # Classification 1: Root directory / missing package.json
    if any(keyword in log_lower for keyword in [
        "couldn't find any `pages` or `app` directory",
        "could not find a next.config",
        "package.json not found",
        "no such file or directory: package.json"
    ]):
        return {
            "category": "root_directory_missing_package",
            "confidence": 0.9,
            "suggested_patch": {
                "type": "config_note",
                "action": "verify_root_directory",
                "message": "Vercel root directory may be incorrect. Verify Root Directory setting in Vercel project settings matches the app location (e.g., 'apps/symbioz-web')."
            },
            "key_errors": key_errors[:5]
        }
    
    # Classification 2: Build command not finding next
    if any(keyword in log_lower for keyword in [
        "command not found: next",
        "'next' is not recognized",
        "next: command not found"
    ]):
        return {
            "category": "next_command_not_found",
            "confidence": 0.95,
            "suggested_patch": {
                "type": "package_json_script",
                "action": "use_npx_next",
                "file": "apps/symbioz-web/package.json",
                "message": "Build scripts should use 'npx next' instead of 'next'"
            },
            "key_errors": key_errors[:5]
        }
    
    # Classification 3: TypeScript nullability errors
    ts_null_pattern = re.search(
        r"type ['\"](.+?)['\"] is not assignable to type ['\"](.+?)['\"].*null",
        log_text,
        re.IGNORECASE
    )
    if ts_null_pattern or any("null" in err.lower() and "type" in err.lower() for err in key_errors):
        # Try to extract file and line
        file_match = re.search(r"([^\s]+\.tsx?)[\(:](\d+)[\):]", log_text)
        if file_match:
            return {
                "category": "typescript_nullability",
                "confidence": 0.85,
                "suggested_patch": {
                    "type": "typescript_fix",
                    "action": "add_null_check",
                    "file": file_match.group(1),
                    "line": int(file_match.group(2)),
                    "message": "TypeScript nullability error detected. May need null check or type guard."
                },
                "key_errors": key_errors[:5]
            }
    
    # Classification 4: Missing environment variable
    env_var_pattern = re.search(r"missing.*env.*var.*['\"](.+?)['\"]", log_text, re.IGNORECASE)
    if env_var_pattern:
        var_name = env_var_pattern.group(1)
        return {
            "category": "missing_env_var",
            "confidence": 0.9,
            "suggested_patch": {
                "type": "env_var_note",
                "action": "add_env_var",
                "var_name": var_name,
                "message": f"Missing environment variable: {var_name}. Add it to Vercel project settings."
            },
            "key_errors": key_errors[:5]
        }
    
    # Classification 5: Install/build command issues
    if any(keyword in log_lower for keyword in [
        "npm ci failed",
        "npm install failed",
        "lockfile",
        "package-lock.json"
    ]):
        return {
            "category": "install_command_issue",
            "confidence": 0.7,
            "suggested_patch": {
                "type": "config_note",
                "action": "check_install_command",
                "message": "Install command may need adjustment. Check package-lock.json exists and install command is correct."
            },
            "key_errors": key_errors[:5]
        }
    
    # Default: unknown failure
    return {
        "category": "unknown",
        "confidence": 0.0,
        "suggested_patch": {
            "type": "diagnosis_only",
            "action": "manual_review",
            "message": "Failure pattern not recognized. Manual review required."
        },
        "key_errors": key_errors[:10]
    }


def parse_render_failure(log_text: str) -> Dict[str, Any]:
    """
    Parse Render deployment failure and classify it.
    
    Returns:
        {
            "category": str,
            "confidence": float (0.0-1.0),
            "suggested_patch": Dict with fix details,
            "key_errors": List[str]
        }
    """
    log_lower = log_text.lower()
    key_errors = []
    
    # Extract key error lines
    for line in log_text.split("\n"):
        if any(keyword in line.lower() for keyword in ["error", "failed", "exception", "traceback"]):
            key_errors.append(line.strip())
    
    # Classification 1: Docker COPY/WORKDIR path errors
    if any(keyword in log_lower for keyword in [
        "copy failed",
        "file not found",
        "no such file or directory",
        "cannot find the file specified"
    ]) and "dockerfile" in log_lower:
        # Try to extract the problematic path
        path_match = re.search(r"copy.*['\"](.+?)['\"]", log_lower)
        return {
            "category": "docker_copy_path",
            "confidence": 0.9,
            "suggested_patch": {
                "type": "dockerfile_fix",
                "action": "fix_copy_path",
                "file": "apps/otto/Dockerfile",
                "message": "Dockerfile COPY path may be incorrect. Verify paths are relative to build context."
            },
            "key_errors": key_errors[:5]
        }
    
    # Classification 2: PORT binding issues
    if any(keyword in log_lower for keyword in [
        "address already in use",
        "cannot bind to port",
        "port.*already",
        "bind.*failed"
    ]):
        return {
            "category": "port_binding",
            "confidence": 0.95,
            "suggested_patch": {
                "type": "dockerfile_fix",
                "action": "use_port_env",
                "file": "apps/otto/Dockerfile",
                "message": "Ensure app binds to $PORT environment variable with fallback."
            },
            "key_errors": key_errors[:5]
        }
    
    # Classification 3: Missing Python module/import
    if any(keyword in log_lower for keyword in [
        "module not found",
        "no module named",
        "import.*error",
        "cannot import"
    ]):
        module_match = re.search(r"no module named ['\"](.+?)['\"]", log_lower)
        if module_match:
            module_name = module_match.group(1)
            return {
                "category": "missing_python_module",
                "confidence": 0.85,
                "suggested_patch": {
                    "type": "requirements_fix",
                    "action": "add_package",
                    "file": "apps/otto/requirements.txt",
                    "package": module_name,
                    "message": f"Missing Python package: {module_name}. May need to add to requirements.txt."
                },
                "key_errors": key_errors[:5]
            }
    
    # Classification 4: Python import path issues
    if "import error" in log_lower or "cannot import" in log_lower:
        return {
            "category": "python_import_path",
            "confidence": 0.7,
            "suggested_patch": {
                "type": "code_fix",
                "action": "check_import_paths",
                "message": "Python import path issue. Verify import statements match package structure."
            },
            "key_errors": key_errors[:5]
        }
    
    # Classification 5: Build context issues
    if "workdir" in log_lower and ("not found" in log_lower or "no such" in log_lower):
        return {
            "category": "docker_workdir",
            "confidence": 0.8,
            "suggested_patch": {
                "type": "dockerfile_fix",
                "action": "fix_workdir",
                "file": "apps/otto/Dockerfile",
                "message": "Dockerfile WORKDIR path may be incorrect."
            },
            "key_errors": key_errors[:5]
        }
    
    # Default: unknown failure
    return {
        "category": "unknown",
        "confidence": 0.0,
        "suggested_patch": {
            "type": "diagnosis_only",
            "action": "manual_review",
            "message": "Failure pattern not recognized. Manual review required."
        },
        "key_errors": key_errors[:10]
    }

