"""
INNERGY API client - typed client built from OpenAPI spec.

This client provides methods to interact with the INNERGY API.
It's built from the OpenAPI specification at integrations/innergy/openapi_innergy.json.

TODO: Update endpoint paths and request/response models based on actual OpenAPI spec.
"""

import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class INNERGYClientError(Exception):
    """Base exception for INNERGY client errors."""
    pass


class INNERGYProject(BaseModel):
    """INNERGY project model - TODO: Update based on OpenAPI spec."""
    id: Optional[str] = None
    project_number: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    # TODO: Add more fields based on OpenAPI spec
    
    class Config:
        extra = "allow"


class INNERGYMaterial(BaseModel):
    """INNERGY material model - TODO: Update based on OpenAPI spec."""
    id: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    # TODO: Add more fields based on OpenAPI spec
    
    class Config:
        extra = "allow"


class INNERGYClient:
    """
    Typed client for INNERGY API.
    
    TODO: Update methods based on actual OpenAPI spec endpoints.
    Currently implements placeholder methods for common operations.
    """
    
    def __init__(self, api_key: str, base_url: str):
        """
        Initialize INNERGY client.
        
        Args:
            api_key: INNERGY API key
            base_url: Base URL for INNERGY API (from OpenAPI spec)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={
                'Authorization': f'Bearer {api_key}',  # TODO: Verify auth header format from OpenAPI spec
                'Content-Type': 'application/json',
            },
            timeout=30.0,
        )
        logger.info(f"Initialized INNERGY client for {self.base_url}")
    
    def _load_openapi_spec(self) -> Optional[Dict[str, Any]]:
        """Load OpenAPI spec from file."""
        spec_path = Path(__file__).parent / 'openapi_innergy.json'
        if not spec_path.exists():
            logger.warning(f"OpenAPI spec not found at {spec_path}")
            return None
        
        try:
            with open(spec_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading OpenAPI spec: {e}")
            return None
    
    def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """Make HTTP request to INNERGY API."""
        try:
            response = self.client.request(method, path, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise INNERGYClientError(f"API request failed: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise INNERGYClientError(f"Request failed: {e}")
    
    def list_projects(self, **query_params) -> List[INNERGYProject]:
        """
        List projects from INNERGY.
        
        TODO: Update endpoint path and query parameters based on OpenAPI spec.
        Expected endpoint: GET /api/projects (or similar)
        
        Args:
            **query_params: Query parameters (e.g., status, limit, offset)
        
        Returns:
            List of INNERGYProject instances
        """
        # TODO: Update path based on OpenAPI spec
        path = '/api/projects'  # Placeholder - verify from OpenAPI spec
        
        try:
            response = self._request('GET', path, params=query_params)
            data = response.json()
            
            # TODO: Update parsing based on actual API response structure
            # Expected: {"projects": [...]} or [...]
            projects_data = data.get('projects', data) if isinstance(data, dict) else data
            
            return [INNERGYProject(**p) for p in projects_data]
        except Exception as e:
            logger.error(f"Error listing projects: {e}")
            raise
    
    def get_project(self, project_id: str) -> Optional[INNERGYProject]:
        """
        Get a single project by ID.
        
        TODO: Update endpoint path based on OpenAPI spec.
        Expected endpoint: GET /api/projects/{project_id}
        
        Args:
            project_id: INNERGY project ID
        
        Returns:
            INNERGYProject instance, or None if not found
        """
        # TODO: Update path based on OpenAPI spec
        path = f'/api/projects/{project_id}'  # Placeholder - verify from OpenAPI spec
        
        try:
            response = self._request('GET', path)
            data = response.json()
            return INNERGYProject(**data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            logger.error(f"Error getting project {project_id}: {e}")
            raise
    
    def list_project_work_orders(self, project_id: str) -> List[Dict[str, Any]]:
        """
        List work orders for a project.
        
        TODO: Update endpoint path based on OpenAPI spec.
        Expected endpoint: GET /api/projects/{project_id}/work-orders (or similar)
        
        Args:
            project_id: INNERGY project ID
        
        Returns:
            List of work order dictionaries
        """
        # TODO: Update path based on OpenAPI spec
        path = f'/api/projects/{project_id}/work-orders'  # Placeholder - verify from OpenAPI spec
        
        try:
            response = self._request('GET', path)
            data = response.json()
            # TODO: Update parsing based on actual API response structure
            return data.get('work_orders', data) if isinstance(data, dict) else data
        except Exception as e:
            logger.error(f"Error listing work orders for project {project_id}: {e}")
            raise
    
    def list_purchase_orders(self, project_id: str) -> List[Dict[str, Any]]:
        """
        List purchase orders for a project.
        
        TODO: Update endpoint path based on OpenAPI spec.
        Expected endpoint: GET /api/projects/{project_id}/purchase-orders (or similar)
        
        Args:
            project_id: INNERGY project ID
        
        Returns:
            List of purchase order dictionaries
        """
        # TODO: Update path based on OpenAPI spec
        path = f'/api/projects/{project_id}/purchase-orders'  # Placeholder - verify from OpenAPI spec
        
        try:
            response = self._request('GET', path)
            data = response.json()
            # TODO: Update parsing based on actual API response structure
            return data.get('purchase_orders', data) if isinstance(data, dict) else data
        except Exception as e:
            logger.error(f"Error listing purchase orders for project {project_id}: {e}")
            raise
    
    def list_materials(self, **query_params) -> List[INNERGYMaterial]:
        """
        List materials from INNERGY.
        
        TODO: Update endpoint path based on OpenAPI spec.
        Expected endpoint: GET /api/materials (or similar)
        
        Args:
            **query_params: Query parameters (e.g., category, active, limit, offset)
        
        Returns:
            List of INNERGYMaterial instances
        """
        # TODO: Update path based on OpenAPI spec
        path = '/api/materials'  # Placeholder - verify from OpenAPI spec
        
        try:
            response = self._request('GET', path, params=query_params)
            data = response.json()
            
            # TODO: Update parsing based on actual API response structure
            materials_data = data.get('materials', data) if isinstance(data, dict) else data
            
            return [INNERGYMaterial(**m) for m in materials_data]
        except Exception as e:
            logger.error(f"Error listing materials: {e}")
            raise
    
    def create_project(self, project_data: Dict[str, Any]) -> INNERGYProject:
        """
        Create a new project in INNERGY.
        
        TODO: Update endpoint path and request body structure based on OpenAPI spec.
        Expected endpoint: POST /api/projects
        
        Args:
            project_data: Project data dictionary
        
        Returns:
            Created INNERGYProject instance
        """
        # TODO: Update path and request body structure based on OpenAPI spec
        path = '/api/projects'  # Placeholder - verify from OpenAPI spec
        
        try:
            response = self._request('POST', path, json=project_data)
            data = response.json()
            return INNERGYProject(**data)
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            raise
    
    def update_project(self, project_id: str, project_data: Dict[str, Any]) -> INNERGYProject:
        """
        Update an existing project in INNERGY.
        
        TODO: Update endpoint path based on OpenAPI spec.
        Expected endpoint: PUT /api/projects/{project_id}
        
        Args:
            project_id: INNERGY project ID
            project_data: Project data dictionary with fields to update
        
        Returns:
            Updated INNERGYProject instance
        """
        # TODO: Update path based on OpenAPI spec
        path = f'/api/projects/{project_id}'  # Placeholder - verify from OpenAPI spec
        
        try:
            response = self._request('PUT', path, json=project_data)
            data = response.json()
            return INNERGYProject(**data)
        except Exception as e:
            logger.error(f"Error updating project {project_id}: {e}")
            raise
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()

