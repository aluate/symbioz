"""Project specification parsing and environment variable resolution."""

import os
import re
from typing import Any, Dict, List, Optional

from infra.utils.yaml_loader import load_project_spec


class ProjectSpecError(Exception):
    """Error in project specification."""


def resolve_env_var_reference(ref: str, provider_configs: Dict[str, Dict]) -> Optional[str]:
    """
    Resolve an environment variable reference.
    
    Supported formats:
    - from_env:VAR_NAME -> Get from environment variable
    - from_provider:provider:project:key -> Get from provider config
    - mirror:VAR_NAME -> Copy from another env var (set in same component)
    
    Args:
        ref: Reference string
        provider_configs: Provider configuration dictionaries
        
    Returns:
        Resolved value or None if not found
    """
    # from_env:VAR_NAME
    if ref.startswith("from_env:"):
        var_name = ref.split(":", 1)[1]
        return os.environ.get(var_name)
    
    # from_provider:provider:project:key
    if ref.startswith("from_provider:"):
        parts = ref.split(":")
        if len(parts) != 4:
            raise ProjectSpecError(f"Invalid provider reference format: {ref}")
        
        _, provider, project, key = parts
        
        if provider not in provider_configs:
            return None
        
        provider_config = provider_configs[provider]
        
        # Navigate nested structure (e.g., projects.catered-by-me.project_ref)
        if provider == "supabase":
            projects = provider_config.get("projects", {})
            if project in projects:
                project_config = projects[project]
                return project_config.get(key)
        
        # Default: look for key at top level
        return provider_config.get(key)
    
    # mirror:VAR_NAME - returns the reference to be resolved later
    if ref.startswith("mirror:"):
        return ref  # Pass through for component-level resolution
    
    # Direct value
    return ref


def resolve_component_env_vars(
    component: Dict[str, Any],
    provider_configs: Dict[str, Dict],
    component_env_vars: Dict[str, str],
) -> Dict[str, str]:
    """
    Resolve all environment variables for a component.
    
    Args:
        component: Component definition from project spec
        provider_configs: Provider configuration dictionaries
        component_env_vars: Already-resolved env vars from this component (for mirror references)
        
    Returns:
        Dictionary of resolved environment variables
    """
    env_vars = {}
    env_var_defs = component.get("env_vars", {})
    
    # First pass: resolve direct and provider references
    for key, ref in env_var_defs.items():
        if isinstance(ref, str):
            resolved = resolve_env_var_reference(ref, provider_configs)
            if resolved is not None:
                env_vars[key] = resolved
        else:
            # Direct value
            env_vars[key] = str(ref)
    
    # Second pass: resolve mirror references
    for key, ref in env_var_defs.items():
        if isinstance(ref, str) and ref.startswith("mirror:"):
            source_var = ref.split(":", 1)[1]
            if source_var in env_vars:
                env_vars[key] = env_vars[source_var]
            elif source_var in component_env_vars:
                env_vars[key] = component_env_vars[source_var]
    
    return env_vars


def validate_project_spec(spec: Dict[str, Any]) -> List[str]:
    """
    Validate a project specification and return list of errors.
    
    Args:
        spec: Project spec dictionary
        
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    # Required fields
    required = ["name", "environment"]
    for field in required:
        if field not in spec:
            errors.append(f"Missing required field: {field}")
    
    # Validate components
    components = spec.get("components", {})
    if not components:
        errors.append("No components defined")
    
    for comp_name, comp_def in components.items():
        if not isinstance(comp_def, dict):
            errors.append(f"Component '{comp_name}' must be a dictionary")
            continue
        
        # Component should have provider
        if "provider" not in comp_def:
            errors.append(f"Component '{comp_name}' missing 'provider' field")
        
        # Component should have repo
        if "repo" not in comp_def:
            errors.append(f"Component '{comp_name}' missing 'repo' field")
    
    return errors


def load_and_validate_project_spec(spec_path: str) -> Dict[str, Any]:
    """
    Load and validate a project specification file.
    
    Args:
        spec_path: Path to project spec YAML file
        
    Returns:
        Validated project spec dictionary
        
    Raises:
        ProjectSpecError: If spec is invalid
    """
    spec = load_project_spec(spec_path)
    errors = validate_project_spec(spec)
    
    if errors:
        error_msg = "Project spec validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
        raise ProjectSpecError(error_msg)
    
    return spec

