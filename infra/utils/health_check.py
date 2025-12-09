"""HTTP health check utilities."""

import time
from typing import Dict, Optional

import httpx


class HealthCheckError(Exception):
    """Error during health check."""


def check_health(
    url: str,
    method: str = "GET",
    expected_status: int = 200,
    timeout: int = 10,
    headers: Optional[Dict[str, str]] = None,
    retries: int = 3,
    retry_delay: float = 1.0,
) -> Dict[str, any]:
    """
    Perform an HTTP health check.
    
    Args:
        url: URL to check
        method: HTTP method (GET, POST, etc.)
        expected_status: Expected HTTP status code
        timeout: Request timeout in seconds
        headers: Optional HTTP headers
        retries: Number of retry attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        Dictionary with health check results:
        {
            "status": "ok" | "warn" | "error",
            "status_code": int,
            "response_time_ms": float,
            "error": str (if error),
            "response_body": str (if available),
        }
    """
    last_error = None
    
    for attempt in range(retries):
        try:
            start_time = time.time()
            
            with httpx.Client(timeout=timeout, headers=headers) as client:
                response = client.request(method, url, follow_redirects=True)
            
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Determine status
            if response.status_code == expected_status:
                status = "ok"
            elif 200 <= response.status_code < 300:
                status = "warn"  # Unexpected but OK status
            else:
                status = "error"
            
            result = {
                "status": status,
                "status_code": response.status_code,
                "response_time_ms": round(response_time, 2),
                "error": None,
            }
            
            # Try to parse response body (limit size)
            try:
                body = response.text
                if len(body) > 1000:
                    body = body[:1000] + "... (truncated)"
                result["response_body"] = body
            except Exception:
                result["response_body"] = None
            
            return result
            
        except httpx.TimeoutException as e:
            last_error = f"Timeout after {timeout}s"
            if attempt < retries - 1:
                time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
        except httpx.RequestError as e:
            last_error = str(e)
            if attempt < retries - 1:
                time.sleep(retry_delay * (attempt + 1))
        except Exception as e:
            last_error = str(e)
            break
    
    # All retries failed
    return {
        "status": "error",
        "status_code": None,
        "response_time_ms": None,
        "error": last_error or "Unknown error",
        "response_body": None,
    }

