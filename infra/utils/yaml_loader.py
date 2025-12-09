"""YAML configuration loading utilities."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def load_yaml(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a YAML file.
    
    Args:
        file_path: Path to YAML file
        
    Returns:
        Parsed YAML content as dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        yaml.YAMLError: If YAML is invalid
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")
    
    with open(path, "r", encoding="utf-8") as f:
        content = yaml.safe_load(f) or {}
    
    return content


def load_config(config_dir: str = "infra") -> Dict[str, Any]:
    """
    Load main config.yaml file.
    
    Args:
        config_dir: Directory containing config.yaml
        
    Returns:
        Config dictionary
    """
    config_path = Path(config_dir) / "config.yaml"
    return load_yaml(str(config_path))


def load_provider_configs(config_dir: str = "infra") -> Dict[str, Dict[str, Any]]:
    """
    Load all provider configuration files.
    
    Args:
        config_dir: Directory containing providers/ folder
        
    Returns:
        Dictionary mapping provider names to their configs
    """
    providers_dir = Path(config_dir) / "providers"
    configs = {}
    
    if not providers_dir.exists():
        return configs
    
    # Load all YAML files in providers directory
    for yaml_file in providers_dir.glob("*.yaml"):
        provider_name = yaml_file.stem
        try:
            configs[provider_name] = load_yaml(str(yaml_file))
        except Exception as e:
            # Log but don't fail - missing provider configs are OK
            print(f"Warning: Could not load provider config {yaml_file}: {e}")
    
    return configs


def load_project_spec(spec_path: str) -> Dict[str, Any]:
    """
    Load a project specification file.
    
    Args:
        spec_path: Path to project spec YAML file
        
    Returns:
        Project spec dictionary
    """
    return load_yaml(spec_path)


def get_env_config(config: Dict[str, Any], env: str) -> Dict[str, Any]:
    """
    Extract environment-specific configuration.
    
    Args:
        config: Full config dictionary
        env: Environment name (e.g., 'dev', 'prod')
        
    Returns:
        Environment-specific config
    """
    environments = config.get("environments", {})
    return environments.get(env, {})


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple config dictionaries (later ones override earlier ones).
    
    Args:
        *configs: Config dictionaries to merge
        
    Returns:
        Merged configuration
    """
    merged = {}
    for config in configs:
        merged.update(config)
    return merged

