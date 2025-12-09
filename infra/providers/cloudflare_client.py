"""Cloudflare DNS provider client for managing DNS records."""

import httpx
from typing import Any, Dict, List, Optional
from .base import BaseProvider, ProviderCheckResult, ProviderStatus


class CloudflareClient(BaseProvider):
    """Client for Cloudflare DNS API."""
    
    API_BASE_URL = "https://api.cloudflare.com/client/v4"
    
    def __init__(self, config: Dict[str, Any], env: str = "prod", dry_run: bool = False):
        """Initialize Cloudflare client."""
        super().__init__(config, env, dry_run)
        self.api_token = config.get("api_token") or self._get_env_var("CLOUDFLARE_API_TOKEN")
        self.email = config.get("email") or self._get_env_var("CLOUDFLARE_EMAIL")
        self.api_key = config.get("api_key") or self._get_env_var("CLOUDFLARE_API_KEY")
    
    def _get_env_var(self, var_name: str) -> Optional[str]:
        """Get environment variable."""
        import os
        return os.getenv(var_name)
    
    def _get_headers(self) -> Dict[str, str]:
        """Get API headers."""
        if self.api_token:
            # Use API token (preferred)
            return {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            }
        elif self.email and self.api_key:
            # Use email + API key (legacy)
            return {
                "X-Auth-Email": self.email,
                "X-Auth-Key": self.api_key,
                "Content-Type": "application/json",
            }
        else:
            raise ValueError("Either CLOUDFLARE_API_TOKEN or CLOUDFLARE_EMAIL + CLOUDFLARE_API_KEY required")
    
    def check_health(self) -> ProviderCheckResult:
        """Check Cloudflare API health."""
        try:
            url = f"{self.API_BASE_URL}/user/tokens/verify"
            headers = self._get_headers()
            
            if self.dry_run:
                return ProviderCheckResult(
                    provider="cloudflare",
                    status=ProviderStatus.OK.value,
                    human_summary="Cloudflare client initialized (dry-run mode)",
                    details={"dry_run": True}
                )
            
            with httpx.Client() as client:
                response = client.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    user_info = response.json().get("result", {})
                    return ProviderCheckResult(
                        provider="cloudflare",
                        status=ProviderStatus.OK.value,
                        human_summary=f"Cloudflare API accessible - User: {user_info.get('email', 'Unknown')}",
                        details={"user": user_info}
                    )
                else:
                    return ProviderCheckResult(
                        provider="cloudflare",
                        status=ProviderStatus.ERROR.value,
                        human_summary=f"Cloudflare API check failed: {response.status_code}",
                        details={"status_code": response.status_code, "response": response.text[:200]}
                    )
        except Exception as e:
            return ProviderCheckResult(
                provider="cloudflare",
                status=ProviderStatus.ERROR.value,
                human_summary=f"Cloudflare API error: {str(e)}",
                details={"error": str(e)}
            )
    
    def get_zone_id(self, domain: str) -> Optional[str]:
        """Get zone ID for a domain."""
        if self.dry_run:
            return "dry-run-zone-id"
        
        url = f"{self.API_BASE_URL}/zones"
        params = {"name": domain}
        
        with httpx.Client() as client:
            try:
                response = client.get(url, headers=self._get_headers(), params=params, timeout=10)
                response.raise_for_status()
                result = response.json()
                zones = result.get("result", [])
                if zones:
                    return zones[0].get("id")
                return None
            except Exception as e:
                raise Exception(f"Failed to get zone ID for {domain}: {str(e)}")
    
    def list_dns_records(self, zone_id: str, name: Optional[str] = None, record_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List DNS records for a zone."""
        if self.dry_run:
            return [{"type": "A", "name": name or "@", "content": "dry-run-content"}]
        
        url = f"{self.API_BASE_URL}/zones/{zone_id}/dns_records"
        params = {}
        if name:
            params["name"] = name
        if record_type:
            params["type"] = record_type
        
        with httpx.Client() as client:
            try:
                response = client.get(url, headers=self._get_headers(), params=params, timeout=10)
                response.raise_for_status()
                result = response.json()
                return result.get("result", [])
            except Exception as e:
                raise Exception(f"Failed to list DNS records: {str(e)}")
    
    def update_dns_record(
        self, 
        zone_id: str, 
        record_id: str, 
        record_type: str, 
        name: str, 
        content: str,
        ttl: int = 1,  # 1 = auto
        proxied: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update an existing DNS record."""
        if self.dry_run:
            return {
                "result": {
                    "id": record_id,
                    "type": record_type,
                    "name": name,
                    "content": content,
                    "ttl": ttl,
                },
                "success": True
            }
        
        url = f"{self.API_BASE_URL}/zones/{zone_id}/dns_records/{record_id}"
        payload = {
            "type": record_type,
            "name": name,
            "content": content,
            "ttl": ttl,
        }
        if proxied is not None:
            payload["proxied"] = proxied
        
        with httpx.Client() as client:
            try:
                response = client.put(url, headers=self._get_headers(), json=payload, timeout=10)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                raise Exception(f"Failed to update DNS record: {str(e)}")
    
    def create_dns_record(
        self,
        zone_id: str,
        record_type: str,
        name: str,
        content: str,
        ttl: int = 1,  # 1 = auto
        proxied: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Create a new DNS record."""
        if self.dry_run:
            return {
                "result": {
                    "id": "dry-run-record-id",
                    "type": record_type,
                    "name": name,
                    "content": content,
                    "ttl": ttl,
                },
                "success": True
            }
        
        url = f"{self.API_BASE_URL}/zones/{zone_id}/dns_records"
        payload = {
            "type": record_type,
            "name": name,
            "content": content,
            "ttl": ttl,
        }
        if proxied is not None:
            payload["proxied"] = proxied
        
        with httpx.Client() as client:
            try:
                response = client.post(url, headers=self._get_headers(), json=payload, timeout=10)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                raise Exception(f"Failed to create DNS record: {str(e)}")
    
    def delete_dns_record(self, zone_id: str, record_id: str) -> bool:
        """Delete a DNS record."""
        if self.dry_run:
            return True
        
        url = f"{self.API_BASE_URL}/zones/{zone_id}/dns_records/{record_id}"
        
        with httpx.Client() as client:
            try:
                response = client.delete(url, headers=self._get_headers(), timeout=10)
                response.raise_for_status()
                return True
            except Exception as e:
                raise Exception(f"Failed to delete DNS record: {str(e)}")
    
    def update_root_domain_to_vercel(
        self, 
        domain: str, 
        vercel_ip: Optional[str] = None,
        vercel_cname: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update root domain DNS record to point to Vercel."""
        zone_id = self.get_zone_id(domain)
        if not zone_id:
            raise Exception(f"Zone not found for domain: {domain}")
        
        # Get existing root domain records
        root_records = self.list_dns_records(zone_id, name=domain, record_type="A")
        
        result = {
            "updated": False,
            "created": False,
            "record_id": None,
            "message": ""
        }
        
        if vercel_ip:
            # Update or create A record
            if root_records:
                # Update existing A record
                record = root_records[0]
                update_result = self.update_dns_record(
                    zone_id=zone_id,
                    record_id=record["id"],
                    record_type="A",
                    name=domain,
                    content=vercel_ip,
                    proxied=False  # DNS only for Vercel
                )
                result["updated"] = True
                result["record_id"] = record["id"]
                result["message"] = f"Updated A record to point to {vercel_ip}"
            else:
                # Create new A record
                create_result = self.create_dns_record(
                    zone_id=zone_id,
                    record_type="A",
                    name=domain,
                    content=vercel_ip,
                    proxied=False
                )
                result["created"] = True
                result["record_id"] = create_result["result"]["id"]
                result["message"] = f"Created A record pointing to {vercel_ip}"
        
        elif vercel_cname:
            # Update or create CNAME record
            # First, check if there's an A record (must delete it first for root domain CNAME)
            if root_records:
                # Delete existing A record(s)
                for record in root_records:
                    self.delete_dns_record(zone_id, record["id"])
            
            # Check if CNAME exists
            cname_records = self.list_dns_records(zone_id, name=domain, record_type="CNAME")
            if cname_records:
                # Update existing CNAME
                record = cname_records[0]
                update_result = self.update_dns_record(
                    zone_id=zone_id,
                    record_id=record["id"],
                    record_type="CNAME",
                    name=domain,
                    content=vercel_cname,
                    proxied=False
                )
                result["updated"] = True
                result["record_id"] = record["id"]
                result["message"] = f"Updated CNAME record to {vercel_cname}"
            else:
                # Create new CNAME
                create_result = self.create_dns_record(
                    zone_id=zone_id,
                    record_type="CNAME",
                    name=domain,
                    content=vercel_cname,
                    proxied=False
                )
                result["created"] = True
                result["record_id"] = create_result["result"]["id"]
                result["message"] = f"Created CNAME record pointing to {vercel_cname}"
        else:
            raise ValueError("Either vercel_ip or vercel_cname must be provided")
        
        return result
