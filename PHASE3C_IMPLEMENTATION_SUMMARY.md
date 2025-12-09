# Phase 3C Implementation Summary: Calendar Integration

## Overview
Phase 3C implements a complete calendar system for Life OS, allowing users to create, manage, and view calendar events. The system is designed with Google Calendar integration in mind (fields for external calendar sync), but currently stores events locally. Future versions can add Google Calendar API integration.

## What Was Built

### 1. Database Model: `CalendarEvent`
**File:** `apps/life_os/backend/models.py`

Added a new model for calendar events with fields:
- `id`, `created_at`, `updated_at`
- `title`, `description`, `start_time`, `end_time`
- `location`, `attendees`, `category`
- `is_recurring`, `recurrence_frequency`, `recurrence_end_date`
- `external_calendar_id`, `external_calendar_type`, `external_sync_enabled` (for future Google Calendar sync)
- `status` (confirmed, tentative, cancelled)
- `reminders` (JSON array of reminder times)

### 2. Calendar API
**File:** `apps/life_os/backend/calendar.py`

RESTful API endpoints:
- `POST /calendar` - Create a new event
- `GET /calendar` - List events (with filters: start_date, end_date, category, status)
- `GET /calendar/upcoming` - Get upcoming events (next N days)
- `GET /calendar/{id}` - Get event details
- `PATCH /calendar/{id}` - Update event
- `DELETE /calendar/{id}` - Delete event
- `GET /calendar/today/summary` - Get summary of today's events and upcoming events

**Special Features:**
- Supports recurring events (daily, weekly, monthly, yearly)
- Reminder system (multiple reminders per event)
- Status management (confirmed, tentative, cancelled)
- Prepared for external calendar sync (Google Calendar fields ready)

### 3. Otto Actions for Calendar
**File:** `apps/life_os/backend/otto/actions.py`

New action handlers:
- **`calendar.create_event`**: Creates a new calendar event
  - Required: `title`, `start_time`
  - Optional: `description`, `end_time`, `location`, `attendees`, `category`, `is_recurring`, `recurrence_frequency`, `reminders`
- **`calendar.update_event`**: Updates an event (including status)
- **`calendar.list_events`**: Lists events with optional filters

### 4. Calendar UI
**File:** `apps/life_os/frontend/app/calendar/page.tsx`

Features:
- **View filters**: Today, Next 7 Days, All Events
- **Create event form**: Full form with all fields including:
  - Title, description, start/end times
  - Location, attendees, category
  - Recurring event setup
  - Multiple reminders (add/remove reminders)
- **Event cards**: Visual display with:
  - Date/time formatting
  - Location, category, attendees badges
  - Recurring event indicator
  - Reminder display
  - Cancel event button
- **Today's summary**: Shows today's events and upcoming events
- **Responsive design** for mobile and desktop
- **Google Calendar note**: Mentions future Google Calendar integration

### 5. Navigation Updates
**File:** `apps/life_os/frontend/app/page.tsx`

Added "Calendar" link to the main Life OS navigation.

## Safety & Integration

### Safety Tiers
- `calendar.create_event`: **TIER_1_LIMITED** (requires basic safety checks)
- `calendar.update_event`: **TIER_1_LIMITED**
- `calendar.list_events`: **TIER_0_SAFE** (read-only)

### Action Severity
- `calendar.create_event`: **MEDIUM** (failure logged, execution continues)
- `calendar.update_event`: **MEDIUM**
- `calendar.list_events`: **LOW** (read-only, failure doesn't affect other actions)

## How to Use

### Via UI
1. Navigate to `/calendar` in Life OS frontend
2. Click "+ New Event" to create an event
3. Use view filters (Today, Next 7 Days, All Events)
4. Click "Cancel Event" to mark an event as cancelled
5. View today's summary for quick overview

### Via Otto
Ask Otto in the Otto Console (`/otto`):
- "Create a calendar event: Meeting with John, tomorrow at 2pm"
- "What events do I have today?"
- "Show me upcoming events this week"
- "Cancel event #5"

Otto will use the `calendar.*` actions to interact with events.

### Via API
```bash
# Create an event
curl -X POST http://localhost:8000/calendar \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "start_time": "2025-01-15T14:00:00",
    "end_time": "2025-01-15T15:00:00",
    "location": "Conference Room A",
    "category": "work",
    "reminders": [{"minutes": 15}, {"minutes": 60}]
  }'

# Get today's summary
curl http://localhost:8000/calendar/today/summary

# Get upcoming events
curl http://localhost:8000/calendar/upcoming?days=7

# Update event status
curl -X PATCH http://localhost:8000/calendar/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "cancelled"}'
```

## Google Calendar Integration (Future)

The system is designed with Google Calendar integration in mind:

### Current State
- Events are stored locally in SQLite
- Fields exist for external calendar sync (`external_calendar_id`, `external_calendar_type`, `external_sync_enabled`)
- UI mentions future Google Calendar integration

### Future Implementation
To add Google Calendar integration:

1. **Install Google Calendar API client**:
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

2. **Add OAuth2 authentication** for Google Calendar access

3. **Create sync service** that:
   - Creates events in Google Calendar when created locally
   - Updates Google Calendar when local events are updated
   - Syncs from Google Calendar to local database (optional)
   - Handles recurring events properly

4. **Add sync settings** in UI to enable/disable Google Calendar sync

5. **Update `calendar.create_event` action** to also create in Google Calendar if `external_sync_enabled` is "yes"

## Testing

### Manual Testing
1. Start all services:
   ```bash
   # Windows
   START_OTTO_WINDOWS.bat
   
   # In another terminal
   cd apps\life_os\backend
   python -m worker.otto_worker
   ```

2. Open `http://localhost:3000/calendar`
3. Create a few test events (including a recurring one)
4. Test view filters
5. Test reminders (add multiple reminders)
6. Cancel an event
7. Test via Otto Console:
   - Go to `http://localhost:3000/otto`
   - Ask: "Create a calendar event: Doctor appointment, next Monday at 10am"
   - Verify it appears in `/calendar`

### Example Otto Prompts
- "Create a calendar event: Team standup, every Monday at 9am, recurring weekly"
- "What events do I have today?"
- "Show me all work events this week"
- "Cancel the meeting on Friday"

## Next Steps

Phase 3 (Core Life OS Features) is now complete! You have:
- ✅ Tasks management (Phase 3A)
- ✅ Bills management (Phase 3B)
- ✅ Calendar integration (Phase 3C)

**Future enhancements:**
- Google Calendar API integration
- Email integration for bill reminders
- SMS notifications for urgent events
- Calendar view (month/week/day views)
- Event search and filtering
- Attendee management
- Event templates

## Files Changed

### Backend
- `apps/life_os/backend/models.py` - Added `CalendarEvent` model
- `apps/life_os/backend/calendar.py` - New API router
- `apps/life_os/backend/main.py` - Registered calendar router
- `apps/life_os/backend/otto/actions.py` - Added calendar action handlers
- `apps/life_os/backend/otto/safety.py` - Added safety tiers for calendar actions

### Frontend
- `apps/life_os/frontend/app/calendar/page.tsx` - New Calendar page
- `apps/life_os/frontend/app/page.tsx` - Added Calendar link

## Notes

- Events are stored in SQLite database (`life_os.db`)
- Recurring events are stored as single events with recurrence metadata (future: expand to instances)
- Reminders are stored as JSON array (e.g., `[{"minutes": 15}, {"minutes": 60}]`)
- External calendar sync fields are ready but not yet implemented
- All calendar operations go through the same safety and action executor pipeline
- The UI is designed to be mobile-friendly for on-the-go event management

