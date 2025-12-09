# Residential SOP Index (Automation Map)

> Source of truth: Residential Cabinets SOP Binder (PDF on server).
> This file is the automation-facing index of that binder.

## Intake & Sales

- **RC-05-01 — Lead Qualification**  
  Goal: qualify or decline, then book Intake.  
  Automations:
  - `systems/intake/lead_tracker_sync.py`
  - `systems/email/email_renderer.py` with lead templates

- **RC-10-01 — New Client Intake**  
  Goal: capture requirements & set expectations before design.  
  Automations:
  - `systems/intake/intake_form_builder.py`
  - `systems/decisions/decisions_from_intake.py`
  - `systems/email/email_renderer.py` (Welcome & Next Steps)

- **RC-10-03 — Initial Estimate**  
  Goal: high-level price with assumptions & allowances.  
  Automations:
  - `systems/contracts/billing_calculator.py`
  - `systems/contracts/contract_model.py`

## Design & CV

- **RC-20-01 — Initial Design Workflow**  
  Automations:
  - `systems/cv/automations/auto_redraw_room.py`
  - `systems/cv/automations/auto_cabinet_place.py`

- **RC-20-02 — Finalize Design & Pricing Pack**  
  Automations:
  - `systems/spec_sheet/spec_sheet_from_decisions.py`
  - `systems/email/email_renderer.py` (Approval to Proceed)

## Engineering & Production

- **RC-30-01 — PM→Engineering Handoff**  
  Automations:
  - `systems/scheduling/backplan_engine.py`
  - `systems/email/email_renderer.py` (Eng Release template)

- **RC-40-03 — Production Package to Shop**  
  Automations:
  - `systems/cv/exporters/to_dxf.py`
  - `systems/cv/exporters/to_json.py`

## Install & Closeout

- **RC-50-01/02 — Install (In-House/Sub)**  
  Automations:
  - `systems/install/install_packet_builder.py`
  - `systems/install/photo_naming_helper.py`

- **RC-60-01 — Punch List**  
  Automations:
  - `systems/install/punch_log_tools.py` (future)

- **RC-70-01 — Closeout**  
  Automations:
  - `systems/contracts/final_billing_tools.py`
  - `systems/email/email_renderer.py` (closeout emails)

## Global

- **RC-90-A — Decisions Checklist** → `systems/decisions/*`
- **RC-90-B — Assumptions & Exclusions** → `systems/contracts/*`
- **RC-90-C — Email Templates** → `systems/email/*`
- **RC-90-G — Folder Tree & Naming** → `systems/intake/lead_tracker_sync.py` + utilities

