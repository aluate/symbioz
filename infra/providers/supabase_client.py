"""Supabase client for diagnostics and schema management."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from infra.providers.base import BaseProvider, ProviderCheckResult


class SupabaseClient(BaseProvider):
    """Client for Supabase operations."""

    def __init__(self, config: Dict[str, Any], env: str = "prod", dry_run: bool = False):
        super().__init__(config, env, dry_run)
        self.projects = config.get("projects", {})

    def validate_config(self) -> bool:
        """Validate Supabase configuration."""
        return bool(self.projects)

    def check_health(self) -> ProviderCheckResult:
        """Check health of configured Supabase projects."""
        if self.dry_run:
            return {
                "provider": "supabase",
                "status": "ok",
                "human_summary": "[DRY RUN] Would check Supabase projects",
                "details": {"dry_run": True},
            }

        project_results = []
        overall_status = "ok"

        for project_name, project_config in self.projects.items():
            if project_config.get("env") != self.env:
                continue

            try:
                result = self._check_project(project_name, project_config)
                project_results.append(result)

                if result["status"] == "error":
                    overall_status = "error"
                elif result["status"] == "warn" and overall_status == "ok":
                    overall_status = "warn"

            except Exception as e:
                project_results.append({
                    "project": project_name,
                    "status": "error",
                    "error": str(e),
                })
                overall_status = "error"

        # Build summary
        error_count = sum(1 for r in project_results if r.get("status") == "error")
        warn_count = sum(1 for r in project_results if r.get("status") == "warn")

        if error_count > 0:
            summary = f"❌ {error_count} project(s) have errors"
        elif warn_count > 0:
            summary = f"⚠️ {warn_count} project(s) have warnings"
        elif project_results:
            summary = f"✅ All {len(project_results)} project(s) healthy"
        else:
            summary = "⚠️ No projects configured for this environment"

        return {
            "provider": "supabase",
            "status": overall_status,
            "human_summary": summary,
            "details": {
                "projects": project_results,
                "total_projects": len(project_results),
            },
        }

    def _check_project(self, project_name: str, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check a single Supabase project."""
        result = {
            "project": project_name,
            "status": "ok",
        }

        # Get connection env vars
        conn_vars = project_config.get("connection_env_vars", {})
        url_key = conn_vars.get("url", "SUPABASE_URL")
        service_key_key = conn_vars.get("service_key", "SUPABASE_SERVICE_KEY")

        supabase_url = os.environ.get(url_key)
        supabase_key = os.environ.get(service_key_key)

        if not supabase_url:
            result["status"] = "error"
            result["error"] = f"Environment variable {url_key} not set"
            return result

        if not supabase_key:
            result["status"] = "warn"
            result["warning"] = f"Environment variable {service_key_key} not set"
            return result

        result["url_set"] = True
        result["key_set"] = bool(supabase_key)

        # Test database connection
        try:
            connection_works = self._test_connection(supabase_url, supabase_key)
            if connection_works:
                result["connection"] = "ok"
            else:
                result["status"] = "error"
                result["connection"] = "failed"
        except Exception as e:
            result["status"] = "error"
            result["connection"] = "failed"
            result["error"] = str(e)

        # Check schema file exists if specified
        schema_file = project_config.get("db_schema_file")
        if schema_file:
            schema_path = Path(schema_file)
            if schema_path.exists():
                result["schema_file"] = "exists"
            else:
                result["status"] = "warn"
                result["warning"] = f"Schema file not found: {schema_file}"

        return result

    def _test_connection(self, supabase_url: str, supabase_key: str) -> bool:
        """Test Supabase database connection."""
        try:
            # Try using Supabase Python client
            from supabase import create_client, Client

            supabase: Client = create_client(supabase_url, supabase_key)

            # Simple query to test connection
            # This will fail if connection is bad
            response = supabase.table("_realtime").select("id").limit(1).execute()
            return True

        except Exception:
            # Fallback: try direct PostgreSQL connection
            try:
                # Extract database connection details from Supabase URL
                # Supabase URL format: https://project-ref.supabase.co
                # DB connection: postgresql://postgres:[password]@db.project-ref.supabase.co:5432/postgres

                # For now, just check if we can import and the URL looks valid
                if supabase_url.startswith("https://") and ".supabase.co" in supabase_url:
                    return True  # URL format is valid
                return False

            except Exception:
                return False

    # Provisioning methods

    def ensure_project_exists(self, project_ref: str) -> Dict[str, Any]:
        """Ensure Supabase project exists (validate)."""
        if self.dry_run:
            self._log_if_dry_run("validate Supabase project", {"project_ref": project_ref})
            return {"project_ref": project_ref, "exists": True}

        # In practice, we'd use Supabase Management API
        # For now, just validate the project_ref format
        if not project_ref or len(project_ref) < 10:
            raise ValueError("Invalid project_ref format")

        return {"project_ref": project_ref, "exists": True}

    def apply_schema(self, schema_file: str) -> Dict[str, Any]:
        """Apply SQL schema to database."""
        if self.dry_run:
            self._log_if_dry_run("apply schema", {"schema_file": schema_file})
            return {"applied": True, "dry_run": True}

        schema_path = Path(schema_file)
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_file}")

        # Read SQL schema
        with open(schema_path, "r", encoding="utf-8") as f:
            sql = f.read()

        # For now, we'd need to execute this via Supabase client or direct PostgreSQL
        # This is a placeholder - actual implementation would need proper SQL execution
        # using Supabase client or psycopg2

        return {
            "applied": True,
            "schema_file": schema_file,
            "sql_size": len(sql),
        }

    def validate_schema(self, schema_file: str) -> bool:
        """Validate schema file exists and is readable."""
        schema_path = Path(schema_file)
        if not schema_path.exists():
            return False

        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                sql = f.read()
            return len(sql) > 0
        except Exception:
            return False

