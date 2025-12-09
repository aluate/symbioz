"""Base provider interface for infrastructure providers."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Literal, Optional, TypedDict


class ProviderStatus(str, Enum):
    """Provider health check status."""

    OK = "ok"
    WARN = "warn"
    ERROR = "error"


class ProviderCheckResult(TypedDict):
    """Result of a provider health check."""

    provider: str
    status: Literal["ok", "warn", "error"]
    human_summary: str
    details: Dict[str, Any]


class BaseProvider(ABC):
    """Base class for all infrastructure providers."""

    def __init__(self, config: Dict[str, Any], env: str = "prod", dry_run: bool = False):
        """
        Initialize provider.
        
        Args:
            config: Provider configuration dictionary
            env: Environment name (dev, staging, prod)
            dry_run: If True, don't make actual API calls
        """
        self.config = config
        self.env = env
        self.dry_run = dry_run
        self.provider_name = self.__class__.__name__.replace("Client", "").lower()

    @abstractmethod
    def check_health(self) -> ProviderCheckResult:
        """
        Check provider health and status.
        
        Returns:
            ProviderCheckResult with status and details
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate provider configuration.
        
        Returns:
            True if config is valid, False otherwise
        """
        pass

    def get_status(self) -> Dict[str, Any]:
        """
        Get current status (default implementation).
        
        Returns:
            Status dictionary
        """
        result = self.check_health()
        return {
            "provider": self.provider_name,
            "status": result["status"],
            "summary": result["human_summary"],
        }

    def _require_env_var(self, var_name: str) -> str:
        """
        Require an environment variable to be set.
        
        Args:
            var_name: Environment variable name
            
        Returns:
            Environment variable value
            
        Raises:
            ValueError: If environment variable is not set
        """
        import os

        value = os.environ.get(var_name)
        if not value:
            raise ValueError(
                f"Required environment variable {var_name} is not set. "
                f"Please set it before running diagnostics."
            )
        return value

    def _log_if_dry_run(self, action: str, details: Optional[Dict] = None):
        """Log action if in dry-run mode."""
        if self.dry_run:
            details_str = f" ({details})" if details else ""
            print(f"[DRY RUN] Would {action}{details_str}")

