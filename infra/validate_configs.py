#!/usr/bin/env python3
"""
Otto Config Validation Script

Validates all configuration files for syntax, structure, and completeness.
Can be run without any API keys or secrets.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Try to import yaml - if not available, we'll provide helpful error
try:
    import yaml
except ImportError:
    print("❌ Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


def validate_yaml_file(file_path: Path) -> Tuple[bool, str, Dict]:
    """
    Validate a YAML file can be loaded and parsed.
    
    Returns:
        (is_valid, error_message, parsed_content)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
        return True, "", content or {}
    except yaml.YAMLError as e:
        return False, f"YAML syntax error: {e}", {}
    except FileNotFoundError:
        return False, f"File not found: {file_path}", {}
    except Exception as e:
        return False, f"Error reading file: {e}", {}


def check_todos(content: Dict, file_path: Path) -> List[str]:
    """Find TODO placeholders in config content."""
    todos = []
    
    def search_dict(d: Any, path: str = ""):
        if isinstance(d, dict):
            for key, value in d.items():
                current_path = f"{path}.{key}" if path else key
                if isinstance(value, str) and "TODO" in value.upper():
                    todos.append(f"{file_path.name}: {current_path} = {value}")
                elif isinstance(value, (dict, list)):
                    search_dict(value, current_path)
        elif isinstance(d, list):
            for i, item in enumerate(d):
                search_dict(item, f"{path}[{i}]")
    
    search_dict(content)
    return todos


def validate_config_structure(config: Dict, required_keys: List[str]) -> List[str]:
    """Check if config has required top-level keys."""
    missing = []
    for key in required_keys:
        if key not in config:
            missing.append(f"Missing required key: {key}")
    return missing


def validate_render_config(config: Dict) -> List[str]:
    """Validate Render provider config structure."""
    errors = []
    
    if "services" not in config:
        errors.append("Missing 'services' section")
        return errors
    
    services = config["services"]
    if not isinstance(services, dict):
        errors.append("'services' must be a dictionary")
        return errors
    
    for service_name, service_config in services.items():
        if not isinstance(service_config, dict):
            errors.append(f"Service '{service_name}' config must be a dictionary")
            continue
            
        required = ["env", "render_service_id", "repo", "branch"]
        for key in required:
            if key not in service_config:
                errors.append(f"Service '{service_name}' missing required field: {key}")
    
    return errors


def validate_supabase_config(config: Dict) -> List[str]:
    """Validate Supabase provider config structure."""
    errors = []
    
    if "projects" not in config:
        errors.append("Missing 'projects' section")
        return errors
    
    projects = config["projects"]
    if not isinstance(projects, dict):
        errors.append("'projects' must be a dictionary")
        return errors
    
    for project_name, project_config in projects.items():
        if not isinstance(project_config, dict):
            errors.append(f"Project '{project_name}' config must be a dictionary")
            continue
        
        if "project_ref" not in project_config:
            errors.append(f"Project '{project_name}' missing 'project_ref'")
        if "connection_env_vars" not in project_config:
            errors.append(f"Project '{project_name}' missing 'connection_env_vars'")
    
    return errors


def validate_stripe_config(config: Dict) -> List[str]:
    """Validate Stripe provider config structure."""
    errors = []
    
    if "projects" not in config:
        errors.append("Missing 'projects' section")
        return errors
    
    projects = config["projects"]
    if not isinstance(projects, dict):
        errors.append("'projects' must be a dictionary")
        return errors
    
    for project_name, project_config in projects.items():
        if not isinstance(project_config, dict):
            errors.append(f"Project '{project_name}' config must be a dictionary")
            continue
        
        if "webhook_endpoint_id" not in project_config:
            errors.append(f"Project '{project_name}' missing 'webhook_endpoint_id'")
    
    return errors


def validate_main_config(config: Dict) -> List[str]:
    """Validate main config.yaml structure."""
    errors = []
    
    if "environments" not in config:
        errors.append("Missing 'environments' section")
    
    if "secrets" not in config:
        errors.append("Missing 'secrets' section")
    elif "required_env_vars" not in config.get("secrets", {}):
        errors.append("Missing 'secrets.required_env_vars' section")
    
    return errors


def validate_project_spec(spec: Dict) -> List[str]:
    """Validate project specification structure."""
    errors = []
    
    required = ["name", "environment", "components"]
    for key in required:
        if key not in spec:
            errors.append(f"Missing required field: {key}")
    
    if "components" in spec:
        components = spec["components"]
        if not isinstance(components, dict):
            errors.append("'components' must be a dictionary")
        else:
            for comp_name, comp_config in components.items():
                if not isinstance(comp_config, dict):
                    errors.append(f"Component '{comp_name}' config must be a dictionary")
                    continue
                if "provider" not in comp_config:
                    errors.append(f"Component '{comp_name}' missing 'provider'")
                if "repo" not in comp_config:
                    errors.append(f"Component '{comp_name}' missing 'repo'")
    
    return errors


def main():
    """Run validation on all config files."""
    print("=" * 60)
    print("Otto Configuration Validation")
    print("=" * 60)
    print()
    
    infra_dir = Path(__file__).parent
    errors_found = []
    warnings_found = []
    todos_found = []
    
    # Validate main config
    print("📄 Validating main config.yaml...")
    config_path = infra_dir / "config.yaml"
    if config_path.exists():
        is_valid, error, content = validate_yaml_file(config_path)
        if not is_valid:
            errors_found.append(f"config.yaml: {error}")
            print(f"  ❌ {error}")
        else:
            config_errors = validate_main_config(content)
            if config_errors:
                errors_found.extend([f"config.yaml: {e}" for e in config_errors])
                print(f"  ❌ {len(config_errors)} structure errors found")
            else:
                print("  ✅ Valid structure")
            
            todos = check_todos(content, config_path)
            todos_found.extend(todos)
            if todos:
                print(f"  ⚠️  {len(todos)} TODO placeholders found")
    else:
        errors_found.append("config.yaml: File not found")
        print("  ❌ File not found")
    
    print()
    
    # Validate provider configs
    providers_dir = infra_dir / "providers"
    if providers_dir.exists():
        for yaml_file in providers_dir.glob("*.yaml"):
            provider_name = yaml_file.stem
            print(f"📄 Validating provider config: {provider_name}.yaml...")
            
            is_valid, error, content = validate_yaml_file(yaml_file)
            if not is_valid:
                errors_found.append(f"{yaml_file.name}: {error}")
                print(f"  ❌ {error}")
                continue
            
            # Provider-specific validation
            if provider_name == "render":
                provider_errors = validate_render_config(content)
            elif provider_name == "supabase":
                provider_errors = validate_supabase_config(content)
            elif provider_name == "stripe":
                provider_errors = validate_stripe_config(content)
            else:
                provider_errors = []
            
            if provider_errors:
                errors_found.extend([f"{yaml_file.name}: {e}" for e in provider_errors])
                print(f"  ❌ {len(provider_errors)} structure errors found")
            else:
                print("  ✅ Valid structure")
            
            # Check for TODOs
            todos = check_todos(content, yaml_file)
            todos_found.extend(todos)
            if todos:
                print(f"  ⚠️  {len(todos)} TODO placeholders found")
            
            print()
    
    # Validate project specs
    specs_dir = infra_dir / "project-specs"
    if specs_dir.exists():
        for yaml_file in specs_dir.glob("*.yaml"):
            print(f"📄 Validating project spec: {yaml_file.name}...")
            
            is_valid, error, content = validate_yaml_file(yaml_file)
            if not is_valid:
                errors_found.append(f"{yaml_file.name}: {error}")
                print(f"  ❌ {error}")
                continue
            
            spec_errors = validate_project_spec(content)
            if spec_errors:
                errors_found.extend([f"{yaml_file.name}: {e}" for e in spec_errors])
                print(f"  ❌ {len(spec_errors)} structure errors found")
            else:
                print("  ✅ Valid structure")
            
            # Check for TODOs
            todos = check_todos(content, yaml_file)
            todos_found.extend(todos)
            if todos:
                print(f"  ⚠️  {len(todos)} TODO placeholders found")
            
            print()
    
    # Summary
    print("=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    if errors_found:
        print(f"\n❌ {len(errors_found)} error(s) found:")
        for error in errors_found:
            print(f"  - {error}")
    else:
        print("\n✅ All configuration files are valid!")
    
    if todos_found:
        print(f"\n⚠️  {len(todos_found)} TODO placeholder(s) found (expected - these need to be filled in):")
        for todo in todos_found[:10]:  # Show first 10
            print(f"  - {todo}")
        if len(todos_found) > 10:
            print(f"  ... and {len(todos_found) - 10} more")
        print("\n💡 Tip: See infra/FINDING_YOUR_KEYS_AND_IDS.md for where to get these values")
    
    print()
    
    if errors_found:
        print("❌ Validation failed. Please fix the errors above.")
        return 1
    else:
        print("✅ Validation passed! Configuration files are ready.")
        if todos_found:
            print("💡 Remember to fill in TODO placeholders before running Otto.")
        return 0


if __name__ == "__main__":
    sys.exit(main())

