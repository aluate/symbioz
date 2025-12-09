"""Auto-fix utilities for providers."""

from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod


class FixResult:
    """Result of an auto-fix attempt."""

    def __init__(
        self,
        success: bool,
        message: str,
        fixes_applied: List[str] = None,
        errors: List[str] = None,
    ):
        self.success = success
        self.message = message
        self.fixes_applied = fixes_applied or []
        self.errors = errors or []


class BaseFixer(ABC):
    """Base class for provider auto-fixers."""

    def __init__(self, provider_client, project_name: str, max_retries: int = 5):
        self.provider = provider_client
        self.project_name = project_name
        self.max_retries = max_retries

    @abstractmethod
    def detect_issues(self) -> List[Dict[str, Any]]:
        """Detect issues that need fixing."""
        pass

    @abstractmethod
    def apply_fixes(self, issues: List[Dict[str, Any]]) -> FixResult:
        """Apply fixes for detected issues."""
        pass

    @abstractmethod
    def trigger_redeploy(self) -> Optional[str]:
        """Trigger a redeployment. Returns deployment ID."""
        pass

    @abstractmethod
    def wait_for_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """Wait for deployment to complete."""
        pass

    def is_deployment_successful(self, deployment: Dict[str, Any]) -> bool:
        """Check if deployment is successful."""
        state = deployment.get("state") or deployment.get("readyState")
        return state in ["READY", "live", "success"]

    def auto_fix_and_retry(self) -> FixResult:
        """Auto-fix issues and retry until successful or max retries."""
        for attempt in range(1, self.max_retries + 1):
            # Detect issues
            issues = self.detect_issues()
            
            if not issues:
                return FixResult(
                    success=True,
                    message=f"✅ No issues detected for {self.project_name}",
                )

            # Apply fixes
            fix_result = self.apply_fixes(issues)
            if not fix_result.success:
                return FixResult(
                    success=False,
                    message=f"❌ Failed to apply fixes: {fix_result.message}",
                    errors=fix_result.errors,
                )

            # Trigger redeploy
            deployment_id = self.trigger_redeploy()
            if not deployment_id:
                return FixResult(
                    success=False,
                    message="❌ Failed to trigger redeployment",
                )

            # Wait for deployment
            try:
                deployment = self.wait_for_deployment(deployment_id)
                if self.is_deployment_successful(deployment):
                    return FixResult(
                        success=True,
                        message=f"✅ Deployment successful after {attempt} attempt(s)",
                        fixes_applied=fix_result.fixes_applied,
                    )
            except Exception as e:
                if attempt == self.max_retries:
                    return FixResult(
                        success=False,
                        message=f"❌ Deployment failed after {attempt} attempts: {e}",
                        errors=[str(e)],
                    )

        return FixResult(
            success=False,
            message=f"❌ Max retries ({self.max_retries}) reached",
        )

