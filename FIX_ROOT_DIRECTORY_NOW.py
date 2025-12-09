#!/usr/bin/env python3
"""Fix root directory for Corporate Crashout - guaranteed output"""

import sys
import os
from pathlib import Path

# Force UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))

# Write to file AND stdout
output_file = Path(__file__).parent / "DEPLOYMENT_RESULT.txt"

def log(msg):
    print(msg)
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

log("=" * 60)
log("FIXING CORPORATE CRASHOUT ROOT DIRECTORY")
log("=" * 60)
log("")

try:
    from dotenv import load_dotenv
    load_dotenv()
    
    vercel_token = os.getenv("VERCEL_TOKEN")
    if not vercel_token:
        log("ERROR: VERCEL_TOKEN not set!")
        log("Add it to .env file")
        sys.exit(1)
    
    log(f"VERCEL_TOKEN: Found ({len(vercel_token)} chars)")
    log("")
    
    log("Loading configuration...")
    from infra.utils.yaml_loader import load_provider_configs
    configs = load_provider_configs()
    vercel_config = configs.get("vercel", {})
    
    if "achillies" not in vercel_config.get("projects", {}):
        log("ERROR: achillies not in config")
        sys.exit(1)
    
    log("Connecting to Vercel API...")
    from infra.providers.vercel_client import VercelClient
    client = VercelClient(vercel_config, env="prod", dry_run=False)
    
    log("Getting project...")
    project = client._get_project("achillies")
    
    if not project:
        log("ERROR: Project 'achillies' not found in Vercel")
        sys.exit(1)
    
    current_root = project.get("rootDirectory")
    expected_root = "apps/corporate-crashout"
    
    log(f"Current root directory: {current_root or '(not set)'}")
    log(f"Expected root directory: {expected_root}")
    log("")
    
    if current_root != expected_root:
        log("FIXING ROOT DIRECTORY...")
        success = client.update_project_settings("achillies", root_directory=expected_root)
        if success:
            log("")
            log("=" * 60)
            log("SUCCESS: Root directory updated!")
            log("=" * 60)
            log("")
            log("Vercel will automatically redeploy.")
            log("Check https://achillies.vercel.app in 2-3 minutes")
        else:
            log("")
            log("=" * 60)
            log("FAILED: Could not update root directory")
            log("=" * 60)
            sys.exit(1)
    else:
        log("Root directory is already correct!")
        log("")
        log("Checking deployment status...")
        deployments = client._list_deployments("achillies", limit=1)
        if deployments:
            latest = deployments[0]
            state = latest.get("state")
            url = latest.get("url")
            log(f"Latest deployment: {state}")
            log(f"URL: {url}")
            if state == "READY":
                log("")
                log("=" * 60)
                log("DEPLOYMENT IS READY!")
                log("=" * 60)
                log(f"Site: https://achillies.vercel.app")
    
    log("")
    log("=" * 60)
    log("DONE!")
    log("=" * 60)
    
except Exception as e:
    log("")
    log("=" * 60)
    log(f"ERROR: {e}")
    log("=" * 60)
    import traceback
    log(traceback.format_exc())
    sys.exit(1)
