"""GitHub client for diagnostics."""

import os
from typing import Any, Dict, List, Optional

from github import Github
from github.GithubException import GithubException

from infra.providers.base import BaseProvider, ProviderCheckResult


class GitHubClient(BaseProvider):
    """Client for GitHub API operations."""

    def __init__(self, config: Dict[str, Any], env: str = "prod", dry_run: bool = False):
        super().__init__(config, env, dry_run)
        self.token = self._require_env_var("GITHUB_TOKEN")
        self.repos = config.get("repos", {})
        
        if not dry_run:
            self.github = Github(self.token)

    def validate_config(self) -> bool:
        """Validate GitHub configuration."""
        return bool(self.repos)

    def check_health(self) -> ProviderCheckResult:
        """Check health of configured GitHub repositories."""
        if self.dry_run:
            return {
                "provider": "github",
                "status": "ok",
                "human_summary": "[DRY RUN] Would check GitHub repos",
                "details": {"dry_run": True},
            }

        repo_results = []
        overall_status = "ok"

        for repo_name, repo_config in self.repos.items():
            try:
                result = self._check_repo(repo_name, repo_config)
                repo_results.append(result)

                if result["status"] == "error":
                    overall_status = "error"
                elif result["status"] == "warn" and overall_status == "ok":
                    overall_status = "warn"

            except Exception as e:
                repo_results.append({
                    "repo": repo_name,
                    "status": "error",
                    "error": str(e),
                })
                overall_status = "error"

        # Build summary
        error_count = sum(1 for r in repo_results if r.get("status") == "error")
        warn_count = sum(1 for r in repo_results if r.get("status") == "warn")

        if error_count > 0:
            summary = f"❌ {error_count} repo(s) have errors"
        elif warn_count > 0:
            summary = f"⚠️ {warn_count} repo(s) have warnings"
        elif repo_results:
            summary = f"✅ All {len(repo_results)} repo(s) healthy"
        else:
            summary = "⚠️ No repos configured"

        return {
            "provider": "github",
            "status": overall_status,
            "human_summary": summary,
            "details": {
                "repos": repo_results,
                "total_repos": len(repo_results),
            },
        }

    def _check_repo(self, repo_name: str, repo_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check a single GitHub repository."""
        result = {
            "repo": repo_name,
            "status": "ok",
        }

        # Get repo from config (format: owner/repo)
        repo_path = repo_config.get("path") or repo_name
        if "/" not in repo_path:
            result["status"] = "error"
            result["error"] = f"Invalid repo path format: {repo_path} (expected owner/repo)"
            return result

        try:
            repo = self.github.get_repo(repo_path)
            result["repo_path"] = repo.full_name
            result["private"] = repo.private
            result["default_branch"] = repo.default_branch

            # Check default branch
            default_branch_name = repo_config.get("default_branch", repo.default_branch)
            try:
                branch = repo.get_branch(default_branch_name)
                result["branch"] = {
                    "name": branch.name,
                    "sha": branch.commit.sha,
                    "commit_message": branch.commit.commit.message[:100] if branch.commit.commit.message else None,
                }
            except GithubException:
                result["status"] = "warn"
                result["warning"] = f"Branch '{default_branch_name}' not found"

            # Check CI/CD status (GitHub Actions)
            ci_provider = repo_config.get("ci_provider", "github-actions")
            if ci_provider == "github-actions":
                try:
                    # Get latest workflow run
                    workflows = repo.get_workflows()
                    if workflows.totalCount > 0:
                        # Get latest run from any workflow
                        latest_run = None
                        for workflow in workflows:
                            runs = workflow.get_runs()
                            if runs.totalCount > 0:
                                run = runs[0]
                                if latest_run is None or run.created_at > latest_run.created_at:
                                    latest_run = run

                        if latest_run:
                            result["ci"] = {
                                "status": latest_run.status,
                                "conclusion": latest_run.conclusion,
                                "created_at": latest_run.created_at.isoformat() if latest_run.created_at else None,
                                "workflow": latest_run.name,
                            }

                            if latest_run.conclusion == "failure":
                                result["status"] = "error"
                            elif latest_run.conclusion in ["cancelled", "neutral"]:
                                result["status"] = "warn" if result["status"] == "ok" else result["status"]

                except GithubException as e:
                    result["warning"] = f"Could not check CI status: {e}"

            # Check for failing checks on default branch
            try:
                # Get commit status
                commit = repo.get_commit(result["branch"]["sha"])
                statuses = commit.get_statuses()
                
                failing_statuses = [s for s in statuses if s.state == "failure"]
                if failing_statuses:
                    result["status"] = "error"
                    result["failing_checks"] = [
                        {"context": s.context, "description": s.description}
                        for s in failing_statuses[:5]  # Limit to 5
                    ]

            except GithubException:
                pass  # Status checks might not be available

        except GithubException as e:
            if e.status == 404:
                result["status"] = "error"
                result["error"] = f"Repository not found: {repo_path}"
            elif e.status == 403:
                result["status"] = "error"
                result["error"] = "Access denied (check GITHUB_TOKEN permissions)"
            else:
                result["status"] = "error"
                result["error"] = f"GitHub API error: {e}"

        return result

    def create_repository(
        self, name: str, description: Optional[str] = None, private: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Create a new GitHub repository."""
        if self.dry_run:
            self._log_if_dry_run("create GitHub repository", {"name": name, "private": private})
            return {
                "name": name,
                "full_name": f"mock/{name}",
                "html_url": f"https://github.com/mock/{name}",
                "private": private,
            }

        try:
            user = self.github.get_user()
            repo = user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=False,  # Don't initialize with README
            )
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "html_url": repo.html_url,
                "clone_url": repo.clone_url,
                "private": repo.private,
            }
        except GithubException as e:
            if e.status == 422:
                # Repository already exists
                try:
                    repo = self.github.get_repo(f"{self.github.get_user().login}/{name}")
                    return {
                        "name": repo.name,
                        "full_name": repo.full_name,
                        "html_url": repo.html_url,
                        "clone_url": repo.clone_url,
                        "private": repo.private,
                        "already_exists": True,
                    }
                except GithubException:
                    pass
            raise

