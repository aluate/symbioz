# Date Format Guidelines for Templates

## Default Format: American (M.D.YYYY)

**For all user-facing dates, use American format unless otherwise specified.**

### Format Standards

1. **User-Facing Dates (Display):**
   - Format: `M.D.YYYY` (e.g., `6.20.2026`)
   - Examples: `6.20.2026`, `12.25.2025`, `1.5.2027`
   - No leading zeros on month or day (unless required for consistency)

2. **Internal/Serial Dates (Data Storage):**
   - Format: ISO 8601 `YYYY-MM-DD` (e.g., `2026-06-20`)
   - Used for: Database storage, API responses, sorting, calculations
   - Always use ISO format for data integrity and sorting

3. **Date with Month Name (Display):**
   - Format: `Month D, YYYY` (e.g., `June 20, 2026`)
   - Use when you want a more readable format
   - Still American format (month before day)

### Implementation

#### JavaScript/TypeScript

Create a date utility file:

```typescript
// lib/dateUtils.ts

/**
 * Format a date string (YYYY-MM-DD) to American format (M.D.YYYY)
 */
export function formatAmericanDate(dateString: string): string {
  const date = new Date(dateString + 'T00:00:00')
  const month = date.getMonth() + 1
  const day = date.getDate()
  const year = date.getFullYear()
  return `${month}.${day}.${year}`
}

/**
 * Format a date string (YYYY-MM-DD) to American format with month name
 */
export function formatAmericanDateWithMonth(dateString: string): string {
  const date = new Date(dateString + 'T00:00:00')
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ]
  const month = monthNames[date.getMonth()]
  const day = date.getDate()
  const year = date.getFullYear()
  return `${month} ${day}, ${year}`
}
```

#### Usage Example

```typescript
import { formatAmericanDate } from '@/lib/dateUtils'

// In your component
const weddingDate = "2026-06-20" // ISO format from config/API
const displayDate = formatAmericanDate(weddingDate) // "6.20.2026"
```

### When to Use Each Format

- **M.D.YYYY** (`6.20.2026`): Compact display, hero sections, cards
- **Month D, YYYY** (`June 20, 2026`): More formal, invitations, detailed pages
- **YYYY-MM-DD** (`2026-06-20`): Always for data storage, API, config files

### Time Format

- **12-hour format** for user-facing times: `4:30 PM`, `12:00 PM`, `11:59 PM`
- **24-hour format** for data storage: `16:30`, `12:00`, `23:59`

### Notes

- Keep ISO format (`YYYY-MM-DD`) in config files and data storage
- Convert to American format only when displaying to users
- This ensures data consistency while meeting user expectations
- If a project specifically needs a different format (e.g., European), document it clearly in the project README

### Template Checklist

When creating a new template that uses dates:

- [ ] Include date formatting utility functions
- [ ] Document date format in template README
- [ ] Use ISO format in config/data files
- [ ] Convert to American format in display components
- [ ] Add examples in template documentation
