"""
Configuration loader for Otto
"""

from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class StorageConfig:
    default_repo_root: str = "."
    reports_dir: str = "reports"


@dataclass
class SafetyConfig:
    auto_apply_repairs: bool = False
    auto_refactor_repo: bool = False


@dataclass
class AppConfig:
    storage: StorageConfig
    safety: SafetyConfig


def load_config(config_path: Optional[Path] = None) -> AppConfig:
    """
    Load Otto configuration from YAML file.
    
    Looks for config in:
    1. Provided config_path
    2. Current working directory / otto_config.yaml
    3. apps/otto/otto_config.yaml
    
    If not found, returns defaults with warnings.
    """
    if config_path is None:
        # Try current directory first
        config_path = Path("otto_config.yaml")
        if not config_path.exists():
            # Try apps/otto/otto_config.yaml
            config_path = Path(__file__).parent.parent / "otto_config.yaml"
    
    if not config_path.exists():
        print(f"Warning: Config file not found at {config_path}. Using defaults.")
        return AppConfig(
            storage=StorageConfig(),
            safety=SafetyConfig()
        )
    
    with open(config_path, "r") as f:
        data = yaml.safe_load(f) or {}
    
    storage_data = data.get("storage", {})
    safety_data = data.get("safety", {})
    
    return AppConfig(
        storage=StorageConfig(
            default_repo_root=storage_data.get("default_repo_root", "."),
            reports_dir=storage_data.get("reports_dir", "reports")
        ),
        safety=SafetyConfig(
            auto_apply_repairs=safety_data.get("auto_apply_repairs", False),
            auto_refactor_repo=safety_data.get("auto_refactor_repo", False)
        )
    )

