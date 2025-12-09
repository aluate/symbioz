"""Secret redaction utilities for safe logging."""

import re
from typing import Any, Dict, List, Union


# Patterns that indicate secrets (keys and values)
SECRET_KEY_PATTERNS = [
    r"api[_-]?key",
    r"token",
    r"secret",
    r"password",
    r"passwd",
    r"pwd",
    r"auth",
    r"credential",
    r"access[_-]?key",
    r"private[_-]?key",
    r"session[_-]?id",
    r"bearer",
]

# Value patterns that look like secrets
SECRET_VALUE_PATTERNS = [
    r"^sk_[a-zA-Z0-9]{32,}$",  # Stripe keys
    r"^pk_[a-zA-Z0-9]{32,}$",  # Stripe publishable keys
    r"^ghp_[a-zA-Z0-9]{36,}$",  # GitHub tokens
    r"^xrb_[a-zA-Z0-9]{40,}$",  # Render keys
    r"^[a-zA-Z0-9]{40,}$",  # Long alphanumeric strings
]


def is_secret_key(key: str) -> bool:
    """Check if a key name suggests it contains a secret."""
    key_lower = key.lower()
    return any(re.search(pattern, key_lower) for pattern in SECRET_KEY_PATTERNS)


def is_secret_value(value: Any) -> bool:
    """Check if a value looks like a secret."""
    if not isinstance(value, str):
        return False
    
    return any(re.match(pattern, value) for pattern in SECRET_VALUE_PATTERNS)


def redact_secrets(data: Union[Dict, List, Any], max_depth: int = 10) -> Union[Dict, List, Any]:
    """
    Recursively redact secrets from a data structure.
    
    Args:
        data: Data structure to redact (dict, list, or primitive)
        max_depth: Maximum recursion depth to prevent infinite loops
        
    Returns:
        Redacted copy of the data structure
    """
    if max_depth <= 0:
        return "*** (max depth reached) ***"
    
    if isinstance(data, dict):
        redacted = {}
        for key, value in data.items():
            # Redact based on key name
            if is_secret_key(str(key)):
                redacted[key] = "***"
            # Redact based on value pattern
            elif is_secret_value(value):
                redacted[key] = "***"
            # Recurse for nested structures
            elif isinstance(value, (dict, list)):
                redacted[key] = redact_secrets(value, max_depth - 1)
            else:
                redacted[key] = value
        return redacted
    
    elif isinstance(data, list):
        return [redact_secrets(item, max_depth - 1) for item in data]
    
    else:
        # For primitives, check if the value itself looks like a secret
        if is_secret_value(data):
            return "***"
        return data


def safe_log_dict(data: Dict, logger=None) -> str:
    """
    Convert a dict to a safe string for logging (secrets redacted).
    
    Args:
        data: Dictionary to convert
        logger: Optional logger to use
        
    Returns:
        String representation with secrets redacted
    """
    import json
    
    redacted = redact_secrets(data)
    try:
        return json.dumps(redacted, indent=2, default=str)
    except (TypeError, ValueError):
        # Fallback for non-serializable data
        return str(redacted)

