import requests
import logging
import json
from typing import Optional, Dict, Any

logger = logging.getLogger("tools")

def api_request(
    url: str, 
    method: str = "GET", 
    headers: Optional[Dict[str, str]] = None, 
    body: Optional[Any] = None
) -> str:
    """
    Makes an HTTP request to a specified URL using the requests library.
    
    Args:
        url: The endpoint URL.
        method: HTTP method (GET, POST, PUT, DELETE, PATCH).
        headers: Optional dictionary of HTTP headers.
        body: Optional request body (will be sent as JSON).
    
    Returns:
        The response body as a string or an error message.
    """
    try:
        method = method.upper()
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body if method != "GET" else None,
            timeout=30
        )
        
        # Raise an exception for 4xx/5xx errors
        response.raise_for_status()
        
        try:
            # Try to return formatted JSON if possible
            return json.dumps(response.json(), indent=2, ensure_ascii=False)
        except ValueError:
            # Return plain text if not JSON
            return response.text
            
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error: {e}")
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection Error: {e}")
        return f"Connection Error: Could not connect to {url}"
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout Error: {e}")
        return "Error: The request timed out."
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        return f"Unexpected Error: {str(e)}"