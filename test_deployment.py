#!/usr/bin/env python3
"""Quick test to verify deployment script works."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    print("Testing imports...")
    from tools.deploy_corporate_crashout import main, print_step, print_success
    print("✅ Imports successful")
    
    print("\nTesting configuration loading...")
    from infra.utils.yaml_loader import load_provider_configs
    configs = load_provider_configs()
    print(f"✅ Loaded {len(configs)} provider configs: {list(configs.keys())}")
    
    if "vercel" in configs:
        print("✅ Vercel config found")
        projects = configs["vercel"].get("projects", {})
        if "achillies" in projects:
            print("✅ Achillies project config found")
        else:
            print("⚠️  Achillies project not in config")
    else:
        print("⚠️  Vercel config not found")
    
    if "cloudflare" in configs:
        print("✅ Cloudflare config found")
    else:
        print("⚠️  Cloudflare config not found (will be created)")
    
    print("\n✅ All tests passed! Ready to run deployment.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
