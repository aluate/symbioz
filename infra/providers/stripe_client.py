"""Stripe client for diagnostics and resource management."""

import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import stripe

from infra.providers.base import BaseProvider, ProviderCheckResult


class StripeClient(BaseProvider):
    """Client for Stripe API operations."""

    def __init__(self, config: Dict[str, Any], env: str = "prod", dry_run: bool = False):
        super().__init__(config, env, dry_run)
        self.api_key = self._require_env_var("STRIPE_SECRET_KEY")
        self.projects = config.get("projects", {})
        
        # Initialize Stripe SDK
        if not dry_run:
            stripe.api_key = self.api_key

    def validate_config(self) -> bool:
        """Validate Stripe configuration."""
        return bool(self.projects)

    def check_health(self) -> ProviderCheckResult:
        """Check health of Stripe webhooks and recent events."""
        if self.dry_run:
            return {
                "provider": "stripe",
                "status": "ok",
                "human_summary": "[DRY RUN] Would check Stripe webhooks",
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

        # Check for recent failed webhook events
        try:
            failed_webhooks = self._get_recent_failed_webhooks()
            if failed_webhooks:
                overall_status = "warn" if overall_status == "ok" else overall_status
                project_results.append({
                    "type": "global_webhook_check",
                    "status": "warn",
                    "failed_webhooks_count": len(failed_webhooks),
                    "failed_webhooks": failed_webhooks[:5],  # Limit to 5
                })
        except Exception as e:
            # Don't fail on this, just log warning
            pass

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
            "provider": "stripe",
            "status": overall_status,
            "human_summary": summary,
            "details": {
                "projects": project_results,
                "total_projects": len(project_results),
            },
        }

    def _check_project(self, project_name: str, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check a single Stripe project."""
        result = {
            "project": project_name,
            "status": "ok",
        }

        # Check webhook endpoint
        webhook_id = project_config.get("webhook_endpoint_id")
        if webhook_id:
            try:
                webhook = stripe.WebhookEndpoint.retrieve(webhook_id)
                result["webhook"] = {
                    "id": webhook.id,
                    "url": webhook.url,
                    "status": webhook.status,
                    "enabled_events_count": len(webhook.enabled_events),
                }

                if webhook.status != "enabled":
                    result["status"] = "warn"
                    result["warning"] = f"Webhook endpoint is {webhook.status}"
            except stripe.error.InvalidRequestError as e:
                result["status"] = "error"
                result["error"] = f"Webhook endpoint not found: {e}"
            except Exception as e:
                result["status"] = "warn"
                result["warning"] = f"Could not check webhook: {e}"

        return result

    def _get_recent_failed_webhooks(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get failed webhook events from the last N hours."""
        try:
            # List events from the last 24 hours
            since = datetime.utcnow() - timedelta(hours=hours)
            since_timestamp = int(since.timestamp())

            events = stripe.Event.list(
                limit=100,
                created={"gte": since_timestamp},
                type="payment_intent.payment_failed",  # Example failure type
            )

            failed = []
            for event in events.data:
                # Check if this is a webhook failure
                if event.type.startswith("payment_intent."):
                    failed.append({
                        "id": event.id,
                        "type": event.type,
                        "created": datetime.fromtimestamp(event.created),
                    })

            return failed
        except Exception:
            return []

    # Provisioning methods

    def ensure_webhook_endpoint(
        self, url: str, events: List[str], description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create or update a webhook endpoint."""
        if self.dry_run:
            self._log_if_dry_run("create/update webhook endpoint", {"url": url, "events": events})
            return {"id": "we_mock", "url": url, "status": "enabled"}

        # Check if webhook already exists for this URL
        existing = None
        try:
            webhooks = stripe.WebhookEndpoint.list(limit=100)
            for webhook in webhooks.data:
                if webhook.url == url:
                    existing = webhook
                    break
        except Exception:
            pass

        payload = {
            "url": url,
            "enabled_events": events,
        }
        if description:
            payload["description"] = description

        if existing:
            # Update existing
            webhook = stripe.WebhookEndpoint.modify(existing.id, **payload)
        else:
            # Create new
            webhook = stripe.WebhookEndpoint.create(**payload)

        return {
            "id": webhook.id,
            "url": webhook.url,
            "status": webhook.status,
            "enabled_events": webhook.enabled_events,
        }

    def ensure_product(self, name: str, description: str = "", price_amount: int = None, price_currency: str = "usd", recurring: str = None, product_spec: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create or update a Stripe product with optional price.
        
        Args:
            name: Product name
            description: Product description
            price_amount: Price in cents (if creating price)
            price_currency: Currency code (default: usd)
            recurring: Recurring interval ("month" or "year")
            product_spec: Optional dict with full spec (for backwards compatibility)
        """
        if product_spec:
            # Legacy mode: use product_spec
            if self.dry_run:
                self._log_if_dry_run("create/update product", product_spec)
                return {"id": "prod_mock", "name": product_spec.get("name")}

            product_id = product_spec.get("id")
            name = product_spec.get("name")
            
            if not name:
                raise ValueError("Product name is required")

            payload = {
                "name": name,
            }
            if "description" in product_spec:
                payload["description"] = product_spec["description"]

            if product_id:
                # Update existing
                product = stripe.Product.modify(product_id, **payload)
            else:
                # Create new
                product = stripe.Product.create(**payload)

            return {
                "id": product.id,
                "name": product.name,
                "description": product.description,
            }
        
        # New mode: use parameters
        if self.dry_run:
            self._log_if_dry_run("create/update product", {"name": name, "description": description})
            return {"id": "prod_mock", "name": name, "price_id": "price_mock" if price_amount else None}

        if not name:
            raise ValueError("Product name is required")

        # Check if product already exists
        existing_product = None
        try:
            products = stripe.Product.list(limit=100)
            for prod in products.data:
                if prod.name == name:
                    existing_product = prod
                    break
        except Exception:
            pass

        # Create or update product
        payload = {
            "name": name,
        }
        if description:
            payload["description"] = description

        if existing_product:
            product = stripe.Product.modify(existing_product.id, **payload)
            product_id = product.id
        else:
            product = stripe.Product.create(**payload)
            product_id = product.id

        result = {
            "id": product_id,
            "name": product.name,
            "description": product.description or "",
            "price_id": None,
        }

        # Create price if requested
        if price_amount:
            price = self.ensure_price(product_id, {
                "amount": price_amount,
                "currency": price_currency,
                "recurring": {"interval": recurring} if recurring else None,
            })
            result["price_id"] = price["id"]
            result["price_amount"] = price_amount
            result["price_currency"] = price_currency
            result["recurring"] = recurring

        return result

    def ensure_price(
        self, product_id: str, price_spec: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create or update a Stripe price."""
        if self.dry_run:
            self._log_if_dry_run("create/update price", {"product_id": product_id, "spec": price_spec})
            return {"id": "price_mock", "product_id": product_id}

        amount = price_spec.get("amount")  # In cents
        currency = price_spec.get("currency", "usd")
        recurring = price_spec.get("recurring")  # Dict with interval, etc.

        payload = {
            "product": product_id,
            "unit_amount": amount,
            "currency": currency,
        }
        if recurring:
            payload["recurring"] = recurring

        # Create new price (prices are immutable, so always create)
        price = stripe.Price.create(**payload)

        return {
            "id": price.id,
            "product_id": price.product,
            "amount": price.unit_amount,
            "currency": price.currency,
        }

