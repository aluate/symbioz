# Residential Automation Roadmap

> Owner: Karl + Frat  
> Purpose: Track every automation idea from the Residential SOPs and from Karl's brain, tie it to code, and show status.  
> Status values: `Idea` / `Scoped` / `Prototyping` / `In Use` / `Deprecated`.

## High-Level Projects

1. Lead & Intake / CRM
2. Decisions & Room Matrix
3. Spec Sheet & CV Bridge
4. Cabinet Vision Geometry & Redraw Tools
5. Estimating, Contracts & Billing
6. Scheduling & Capacity / Back-Planning
7. Email & Client Communication Engine
8. Install & Field Tools
9. Warranty / Service & Cost of Quality
10. Reporting, WIP & Dashboards
11. Trim Takeoff & Finish Pricing
12. Meta: Repo Maintenance & SOP Generator

---

## Automation Table

| ID               | Project                          | SOP Ref(s)                      | Name                              | Goal                                                     | Code Path (planned)                                          | Status  |
|------------------|----------------------------------|---------------------------------|-----------------------------------|----------------------------------------------------------|--------------------------------------------------------------|--------|
| AUTO-INT-01      | Lead & Intake                    | RC-05-01, RC-10-01              | Lead Intake Helper                | Capture lead + normalize + write JSON/CSV.              | systems/intake/intake_form_builder.py                        | Idea   |
| AUTO-INT-02      | Lead & Intake                    | RC-05-01                        | Lead Qualification Scoring        | Score leads (Qual / No-Quote / Wait List).              | systems/intake/lead_tracker_sync.py                          | Idea   |
| AUTO-INT-03      | Lead & Intake                    | RC-10-01                        | Intake Packet Builder             | Generate intake docs + client email.                    | systems/intake/intake_form_builder.py                        | Idea   |
| AUTO-INT-04      | Lead & Intake                    | RC-90-G                         | Job Folder & Naming Creator       | Build folder tree + standard filenames.                 | systems/intake/lead_tracker_sync.py                          | Idea   |
| AUTO-DEC-01      | Decisions & Room Matrix          | RC-10-02, RC-90-A               | Intake → Decisions Bridge         | Turn Intake JSON into RC-90-A draft.                    | systems/decisions/decisions_from_intake.py                   | Idea   |
| AUTO-DEC-02      | Decisions & Room Matrix          | RC-90-A, RC-90-J/K/L            | Room Matrix Generator             | Normalize rooms for estimating & scheduling.            | systems/decisions/decisions_model.py                         | Idea   |
| AUTO-DEC-03      | Decisions & Room Matrix          | RC-90-A                         | Complexity Ranker                 | Assign simple/standard/complex per room.                | systems/decisions/complexity_ranker.py                       | Idea   |
| AUTO-SPEC-01     | Spec Sheet & CV Bridge           | RC-14-01/02, RC-20-02           | Spec Sheet Builder                | Generate CV spec sheet from Decisions + Room Matrix.    | systems/spec_sheet/spec_sheet_from_decisions.py              | Idea   |
| AUTO-SPEC-02     | Spec Sheet & CV Bridge           | RC-20-02, RC-90-B               | Spec/Scope Cross-Checker          | Compare spec sheet vs decisions/contract allowances.    | systems/spec_sheet/spec_sheet_model.py                       | Idea   |
| AUTO-SPEC-03     | Spec Sheet & CV Bridge           | RC-32-01                        | Measure Delta Helper              | Turn field measure deltas into CV change actions.       | systems/spec_sheet/spec_sheet_model.py                       | Idea   |
| AUTO-CV-01       | CV Geometry & Redraw             | RC-20-02, RC-30-01              | CV Room Auto-Redraw               | Rebuild plan/elevations from CV exports.                | systems/cv/automations/auto_redraw_room.py                   | Idea   |
| AUTO-CV-02       | CV Geometry & Redraw             | RC-20-02                        | CV Scene Validator                | Detect anchored/mirrored/off-grid CV weirdness.         | systems/cv/automations/cv_scene_validator.py                 | Idea   |
| AUTO-CV-03       | CV Geometry & Redraw             | RC-30-01                        | DXF Cleaner & Exporter            | Clean DXFs into shop/architect-ready files.             | systems/cv/exporters/to_dxf.py                               | Idea   |
| AUTO-CV-04       | CV Geometry & Redraw             | RC-32-01                        | Post-Measure Reconciliation       | Apply deltas to geometry + generate change report.      | systems/cv/automations/cv_delta_apply.py                     | Idea   |
| AUTO-EST-01      | Estimating & Contracts           | RC-14-01/02                     | Estimate Calculator               | Generate estimates from room matrix + spec level.       | systems/contracts/billing_calculator.py                      | Idea   |
| AUTO-CONTRACT-01 | Estimating & Contracts           | RC-80-01, RC-90-B               | Contract Generator                | Turn estimate + assumptions into contract doc.          | systems/contracts/contract_generator.py                      | Idea   |
| AUTO-BILL-01     | Estimating & Contracts           | RC-80-01                        | Billing Milestone Calculator      | Calculate deposit/progress/final payments.              | systems/contracts/billing_calculator.py                      | Idea   |
| AUTO-SCHED-01    | Scheduling & Capacity            | RC-15-01, RC-40-02              | Back-Plan Engine                  | Build internal dates from target install.               | systems/scheduling/backplan_engine.py                        | Idea   |
| AUTO-SCHED-02    | Scheduling & Capacity            | RC-35-01, RC-40-01/03/04/05     | Capacity Checker                  | Flag overbooked weeks based on current jobs.            | systems/scheduling/capacity_model.py                         | Idea   |
| AUTO-SCHED-03    | Scheduling & Capacity            | RC-40-02                        | Client Timeline Export            | Client-facing milestone calendar.                       | systems/scheduling/client_timeline_export.py                 | Idea   |
| AUTO-EMAIL-01    | Email & Communication            | RC-90-C                         | Email Template Renderer           | Fill RC-90-C templates from job metadata.               | systems/email/email_renderer.py                              | Idea   |
| AUTO-EMAIL-02    | Email & Communication            | RC-10-01, RC-14-01, RC-40-02    | Stage-Based Email Wizard          | Suggest/send correct email when job stage changes.      | systems/email/email_batch_tools.py                           | Idea   |
| AUTO-EMAIL-03    | Email & Communication            | RC-40-02, RC-70-01              | Batch Update Sender               | Weekly updates to multiple clients from WIP data.       | systems/email/email_batch_tools.py                           | Idea   |
| AUTO-INSTALL-01  | Install & Field Tools            | RC-50-01/02                     | Install Packet Builder            | Merge plans/notes into installer packet PDF.            | systems/install/install_packet_builder.py                    | Idea   |
| AUTO-INSTALL-02  | Install & Field Tools            | RC-50-Prep                      | Site Readiness Checklist          | Check jobsite meets pre-install requirements.           | systems/install/site_readiness_checker.py                    | Idea   |
| AUTO-INSTALL-03  | Install & Field Tools            | RC-50-01/02, RC-60-01           | Photo Naming Helper               | Help installers name photos consistently.               | systems/install/photo_naming_helper.py                       | Idea   |
| AUTO-WARR-01     | Warranty & CoQ                   | Warranty SOPs                   | Warranty Intake Parser            | Turn emails into structured service tickets.            | systems/warranty/warranty_intake_parser.py                   | Idea   |
| AUTO-WARR-02     | Warranty & CoQ                   | Warranty SOPs                   | Service Ticket Log & Metrics      | Track visits/time/materials, export CoQ metrics.        | systems/warranty/service_ticket_model.py                     | Idea   |
| AUTO-WARR-03     | Warranty & CoQ                   | Warranty SOPs                   | Warranty Response Helper          | Suggest response templates based on rules.              | systems/warranty/warranty_email_flows.py                     | Idea   |
| AUTO-REP-01      | Reporting & Dashboards           | WIP / KPI sections              | Job Snapshot Generator            | Per-job summary of status/money/risks.                  | systems/reporting/job_snapshot.py                            | Idea   |
| AUTO-REP-02      | Reporting & Dashboards           | WIP / KPI sections              | Weekly WIP Dashboard              | Roll-up of all active jobs.                             | systems/reporting/wip_dashboard.py                           | Idea   |
| AUTO-REP-03      | Reporting & Dashboards           | WIP / KPI sections              | KPI Extractor                     | Throughput, hit rate, cycle times, defects, etc.        | systems/reporting/kpi_extractor.py                           | Idea   |
| AUTO-TRIM-01     | Trim Takeoff & Finish Pricing    | Trim SOP (external)             | Trim Takeoff Normalizer           | Turn raw counts/lengths into assemblies.                | systems/trim/takeoff_engine.py                               | Idea   |
| AUTO-TRIM-02     | Trim Takeoff & Finish Pricing    | Trim SOP (external)             | Trim Pricing Engine               | Use Finish Rates & material prices for pricing.         | systems/trim/pricing_engine.py                               | Idea   |
| AUTO-TRIM-03     | Trim Takeoff & Finish Pricing    | Trim SOP (external)             | Mobile Trim App Backend           | API for a phone-friendly trim calculator.               | systems/trim/api.py                                          | Idea   |
| AUTO-TRIM-04     | Trim Takeoff & Finish Pricing    | Trim SOP (external)             | Trim Quote Exporter               | Push trim results into invoices/quotes.                 | systems/trim/exporters.py                                    | Idea   |
| AUTO-META-01     | Meta / Repo Maintenance          | -                               | Roadmap Sync Tool                 | Keep this file & CSV in sync with code.                 | control/tools/roadmap_sync.py                                | Idea   |
| AUTO-META-02     | Meta / Repo Maintenance          | -                               | SOP Draft Generator               | Generate SOP drafts from code + comments.               | control/tools/sop_generator.py                               | Idea   |
| AUTO-META-03     | Meta / Repo Maintenance          | -                               | Tool Catalog CLI                  | List all AUTO-* tools and status.                       | apps/cli/cli.py                                              | Idea   |

---

## Priority Notes

- **P1 (first wave):**
  - AUTO-TRIM-01, AUTO-TRIM-02, AUTO-TRIM-03  → Trim takeoff + mobile-friendly app.
  - AUTO-DEC-01, AUTO-SPEC-01                 → Intake → Decisions → Spec bridge.
  - AUTO-CV-01                                → CV room auto-redraw proof of concept.

- **P2 (second wave):**
  - AUTO-CONTRACT-01, AUTO-BILL-01
  - AUTO-EMAIL-01, AUTO-EMAIL-02
  - AUTO-SCHED-01

Update these priorities as we learn.

---

## Working Rules

- Every new automation gets an `AUTO-` ID and a row in the table.  
- When an automation becomes real (first working script), update **Status** from `Idea` → `Prototyping`.  
- When it is used by humans in the department, set status to `In Use` and write a short how-to in `control/playbooks/`.  
- Karl’s scratch ideas live in a separate file (`control/karl-brain.md`) and only move here once we’ve agreed they are real projects.
