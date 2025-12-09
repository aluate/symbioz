#!/usr/bin/env python3
"""
Basic validation test for Infra/SRE Bot.
Tests imports, config loading, and basic functionality without API calls.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from infra.providers.base import BaseProvider, ProviderCheckResult, ProviderStatus
        print("  ✅ Provider base imports")
        
        from infra.providers.render_client import RenderClient
        print("  ✅ Render client imports")
        
        from infra.providers.supabase_client import SupabaseClient
        print("  ✅ Supabase client imports")
        
        from infra.providers.stripe_client import StripeClient
        print("  ✅ Stripe client imports")
        
        from infra.providers.github_client import GitHubClient
        print("  ✅ GitHub client imports")
        
        from infra.utils.secrets import redact_secrets
        print("  ✅ Secrets utils imports")
        
        from infra.utils.yaml_loader import load_config, load_provider_configs
        print("  ✅ YAML loader imports")
        
        from infra.utils.project_spec import load_and_validate_project_spec
        print("  ✅ Project spec imports")
        
        from infra.utils.health_check import check_health
        print("  ✅ Health check imports")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False


def test_config_loading():
    """Test config file loading."""
    print("\nTesting config loading...")
    
    try:
        from infra.utils.yaml_loader import load_config, load_provider_configs
        
        # Try to load config (might not exist, that's OK)
        try:
            config = load_config()
            print("  ✅ Main config loaded")
        except FileNotFoundError:
            print("  ⚠️  Config file not found (expected if not set up yet)")
        
        # Try to load provider configs
        try:
            provider_configs = load_provider_configs()
            print(f"  ✅ Loaded {len(provider_configs)} provider config(s)")
        except Exception as e:
            print(f"  ⚠️  Could not load provider configs: {e}")
        
        print("\n✅ Config loading test complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Config loading error: {e}")
        return False


def test_secret_redaction():
    """Test secret redaction functionality."""
    print("\nTesting secret redaction...")
    
    try:
        from infra.utils.secrets import redact_secrets
        
        test_data = {
            "api_key": "sk_live_1234567890abcdef",
            "normal_field": "normal_value",
            "password": "secret123",
            "nested": {
                "token": "ghp_abcdef1234567890",
                "safe": "public_data",
            },
        }
        
        redacted = redact_secrets(test_data)
        
        assert redacted["api_key"] == "***"
        assert redacted["normal_field"] == "normal_value"
        assert redacted["password"] == "***"
        assert redacted["nested"]["token"] == "***"
        assert redacted["nested"]["safe"] == "public_data"
        
        print("  ✅ Secret redaction works correctly")
        print("\n✅ Secret redaction test complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Secret redaction error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_dry_run_mode():
    """Test dry-run mode (should work without API keys)."""
    print("\nTesting dry-run mode...")
    
    try:
        from infra.providers.render_client import RenderClient
        from infra.providers.supabase_client import SupabaseClient
        
        # Test Render client in dry-run mode
        render_config = {"services": {}}
        render_client = RenderClient(render_config, env="prod", dry_run=True)
        result = render_client.check_health()
        assert result["status"] in ["ok", "warn", "error"]
        print("  ✅ Render client dry-run works")
        
        # Test Supabase client in dry-run mode
        supabase_config = {"projects": {}}
        supabase_client = SupabaseClient(supabase_config, env="prod", dry_run=True)
        result = supabase_client.check_health()
        assert result["status"] in ["ok", "warn", "error"]
        print("  ✅ Supabase client dry-run works")
        
        print("\n✅ Dry-run mode test complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Dry-run test error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Infra/SRE Bot - Basic Validation Test")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Config Loading", test_config_loading()))
    results.append(("Secret Redaction", test_secret_redaction()))
    results.append(("Dry-Run Mode", test_dry_run_mode()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

