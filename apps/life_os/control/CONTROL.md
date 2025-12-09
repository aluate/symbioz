# Life OS - Control Document

**Purpose:** Define the Life OS household management application architecture, features, and integration points.

## Vision

Life OS is the central hub for personal automation and household management. It provides:
- Kanban-style task management (like CateredByMe swim lanes but for life tasks)
- Integration with Otto for automation
- Calendar, bills, income tracking
- Tax preparation support
- Future: Audiobook Studio, advanced automation

## Core Principles

1. **Task-First:** Everything revolves around tasks and kanban boards
2. **Otto Integration:** Otto handles automation and repetitive work
3. **Household Focus:** Personal use, not public-facing
4. **Extensible:** Modules can be added (Tax Brain, Audiobook Studio, etc.)

## Architecture

### Backend (FastAPI)
- REST API for tasks, calendar, finances
- Database models for tasks, bills, income, transactions
- Integration endpoints for Otto
- Tax Brain module (separate but integrated)

### Frontend (Next.js)
- Kanban board UI (React components)
- Dashboard for overview
- Calendar view
- Financial tracking UI
- Admin panel

### Integration Points
- **Otto:** Task intake, automation, reporting
- **Calendar:** Google Calendar or similar
- **Email/Text:** Scanning for todos
- **Banking:** Transaction import (future)

## Data Models

### Tasks
- Title, description, status (todo/in-progress/done)
- Assignee, due date, priority
- Category/tags
- Linked to kanban board columns

### Bills
- Name, amount, due date, frequency
- Paid status, payment method
- Category for tax purposes

### Income
- Source, amount, frequency
- Date received
- Category for tax purposes

### Transactions
- Date, amount, vendor, description
- Tax category (via Tax Brain)
- Source (manual, import, etc.)

## Modules

### Tax Brain
See `apps/life_os/tax/` for detailed Tax Brain module documentation.

### Audiobook Studio (Future)
See `residential_repo/control/CONTROL_AUDIO.md` for audiobook system.

## Development Status

**Current:** Initial setup - structure being created  
**Next:** Core kanban board, Otto integration

