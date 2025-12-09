#!/usr/bin/env python3
"""Use Otto's deployment automation to check and fix."""

import os
import sys
from pathlib import Path

# Set tokens
os.environ["VERCEL_TOKEN"] = "n6QnE86DsiIcQXIdQp0SA34P"
os.environ["CLOUDFLARE_API_TOKEN"] = "bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH"

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

# Import and run deployment script
from tools.deploy_corporate_crashout import main

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 Running Otto Deployment Automation")
    print("="*70 + "\n")
    main()
