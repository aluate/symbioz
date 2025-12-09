# Snow Load Data Source - Design Document

## Overview

This document outlines the approach for implementing dynamic snow load lookup functionality in the Pole Barn Calculator.

## Current Status

**Phase 1 (Current):** Manual input only
- User enters required snow load (psf) directly
- User can flag "snow load unknown" for future lookup
- Placeholder "Look up Snow Load" button in GUI (non-functional)

**Phase 2 (Future):** Dynamic lookup integration
- Wire lookup button to external data source
- Auto-fill required snow load based on address/location
- Fallback to manual entry if lookup fails

---

## Design Principles

1. **No hard-coded data** - Use external, updatable data sources
2. **Configurable provider** - Support multiple data sources
3. **Graceful degradation** - Always allow manual entry
4. **Desktop-friendly** - Works in bundled exe (may require internet connection)

---

## Architecture

### Interface Design

```python
from typing import Protocol

class SnowLoadProvider(Protocol):
    """Interface for snow load lookup services."""
    
    def lookup(
        self, 
        address: str, 
        zipcode: str | None = None,
        state: str | None = None
    ) -> float:
        """
        Look up snow load for a given location.
        
        Args:
            address: Street address or location description
            zipcode: Optional ZIP code
            state: Optional state abbreviation
            
        Returns:
            Snow load in psf (pounds per square foot)
            
        Raises:
            LookupError: If lookup fails or location not found
        """
        ...
```

### Three Modes of Operation

1. **Manual Mode** (Current)
   - User types required snow load directly
   - No external calls
   - Always available

2. **Semi-Auto Mode** (Future)
   - User clicks "Look up Snow Load" button
   - App calls configurable HTTP endpoint/API
   - Auto-fills required snow load field
   - Falls back to manual if lookup fails

3. **Offline Mode** (Future)
   - If lookup fails or no internet, use manual entry
   - Cache last successful lookup (optional)
   - Never blocks user from proceeding

---

## Potential Data Sources

### Option 1: ICC/ASCE Tools
- **Source:** International Code Council / ASCE 7 standards
- **Access:** Web API or lookup service
- **Coverage:** Nationwide, code-compliant
- **Pros:** Authoritative, standards-based
- **Cons:** May require API key or subscription

### Option 2: State-Specific Maps
- **Source:** State building code offices (e.g., Idaho Building Code)
- **Access:** State-specific APIs or lookup tools
- **Coverage:** State-specific, may be more detailed
- **Pros:** Local accuracy, official sources
- **Cons:** Requires state-by-state integration

### Option 3: Local Building Department APIs
- **Source:** Municipal building departments
- **Access:** City/county APIs
- **Coverage:** Very local, jurisdiction-specific
- **Pros:** Most accurate for permit requirements
- **Cons:** Fragmented, not all jurisdictions have APIs

### Option 4: Third-Party Services
- **Source:** Commercial weather/climate data providers
- **Access:** Paid API services
- **Coverage:** Comprehensive, maintained
- **Pros:** Reliable, well-maintained
- **Cons:** Cost, dependency on external service

### Option 5: Custom Service Layer
- **Source:** Your own service that aggregates multiple sources
- **Access:** Your own HTTP endpoint
- **Coverage:** Configurable
- **Pros:** Full control, can switch sources
- **Cons:** Requires maintaining your own service

---

## Recommended Approach

### Phase 1 (Now): Manual Input
- ✅ Already implemented in changelog entry [11]
- User enters snow load directly
- "Snow load unknown" flag for documentation

### Phase 2 (Future): Configurable Lookup
1. **Add configuration file:** `config/snow_load_provider.json`
   ```json
   {
     "provider": "custom",
     "endpoint": "https://your-service.com/api/snowload",
     "api_key": null,
     "timeout_seconds": 5,
     "enabled": true
   }
   ```

2. **Implement provider interface:**
   - Create `SnowLoadProvider` protocol
   - Implement concrete providers (HTTP, local lookup, etc.)
   - Add provider factory based on config

3. **Wire GUI button:**
   - "Look up Snow Load" button calls provider
   - Shows loading state
   - Handles errors gracefully
   - Auto-fills field on success

4. **Add address input:**
   - Optional address field in GUI
   - Used for lookup if provided
   - Can be stored in project metadata

### Phase 3 (Future): Enhanced Features
- Cache successful lookups
- Batch lookup for multiple projects
- Historical snow load data
- Integration with permit applications

---

## Implementation Notes

### For Desktop Exe
- HTTP requests require internet connection
- Use `requests` library (already available via pandas dependencies)
- Handle network errors gracefully
- Consider offline mode detection

### Configuration
- Store provider config in `config/` directory
- Allow users to update endpoint without rebuilding
- Support multiple provider types via config

### Error Handling
- Network timeouts (5-10 second limit)
- Invalid address/location
- Service unavailable
- Invalid response format
- Always fall back to manual entry

### Security
- API keys stored in config (not hardcoded)
- HTTPS for all external calls
- No sensitive data in logs
- User consent for external lookups

---

## Example Provider Implementation

```python
# Example: HTTP-based provider
import requests
from typing import Optional

class HTTPSnowLoadProvider:
    def __init__(self, endpoint: str, api_key: Optional[str] = None):
        self.endpoint = endpoint
        self.api_key = api_key
    
    def lookup(self, address: str, zipcode: Optional[str] = None) -> float:
        params = {"address": address}
        if zipcode:
            params["zipcode"] = zipcode
        
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = requests.get(
                self.endpoint,
                params=params,
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            return float(data["snow_load_psf"])
        except Exception as e:
            raise LookupError(f"Failed to lookup snow load: {e}")
```

---

## Next Steps

1. ✅ **Complete Phase 1:** Manual input fields (changelog entry [11])
2. ⏳ **Research data sources:** Identify preferred provider(s)
3. ⏳ **Design provider interface:** Create protocol and base implementation
4. ⏳ **Add configuration:** Create config file structure
5. ⏳ **Wire GUI:** Connect lookup button to provider
6. ⏳ **Test & validate:** Ensure lookup works in desktop exe

---

*Document created: Testing Round 1 - Future enhancement planning*

