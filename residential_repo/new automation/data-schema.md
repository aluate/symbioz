# Data Schema — Automation Template

## Entity: SubmissionRecord
- id: string (uuid)
- name: string
- address: string
- email: string
- phone: string
- submitted_at: datetime

## Validation Rules
- Email must contain '@'
- Phone must be 10 digits (or formatted variations)
- Name required
- Address required

## Storage Options
### Option A — JSON file
### Option B — SQLite table
### Option C — Google Sheet integration

## API Payload Example

{
  "name": "John Doe",
  "address": "123 Main St",
  "email": "john@example.com",
  "phone": "208-555-2933"
}
