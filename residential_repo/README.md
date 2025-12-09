residential-ops-automation/
│
├── README.md                     # High-level "what this repo is"
├── docs/
│   ├── SOP_INDEX.md              # Human-readable map of RC codes + summaries
│   ├── RESIDENTIAL_SOP_NOTES.md  # Notes tying PDF binder to automations
│   └── prompts/                  # AI prompts used in Cursor, Claude, etc.
│       ├── cv-interpreter.md
│       ├── intake-helper.md
│       ├── contract-generator.md
│       ├── email-templates-runner.md
│       └── spec-sheet-builder.md
│
├── control/
│   ├── automation-roadmap.md     # MASTER CONTROL DOC (living doc)
│   ├── automation-status.csv     # Simple table Status/Owner/Path
│   └── playbooks/                # Per-system "how to use the tools"
│       ├── intake-playbook.md
│       ├── cv-playbook.md
│       ├── contracts-playbook.md
│       ├── email-playbook.md
│       └── spec-sheet-playbook.md
│
├── systems/                      # Each big workflow in your SOP binder
│   ├── intake/                   # RC-05, RC-10, lead qualification, intake
│   │   ├── models.py
│   │   ├── intake_form_builder.py
│   │   ├── lead_tracker_sync.py
│   │   └── templates/            # Form/email templates, CSV layouts
│   │
│   ├── decisions/                # RC-90-A, complexity ranking, Room Matrix
│   │   ├── decisions_model.py
│   │   ├── decisions_from_intake.py
│   │   └── complexity_ranker.py
│   │
│   ├── spec_sheet/               # CV spec sheet, edgeband-driven sheet, etc.
│   │   ├── spec_sheet_model.py
│   │   ├── spec_sheet_from_decisions.py
│   │   └── excel_layouts/        # .xlsx templates
│   │
│   ├── cv/                       # All the Cabinet Vision trick shit
│   │   ├── parsers/
│   │   │   ├── report_parser.py
│   │   │   ├── xml_parser.py
│   │   │   └── dxf_cleaner.py
│   │   ├── geometry/
│   │   │   ├── model.py
│   │   │   ├── infer.py
│   │   │   └── normalize.py
│   │   ├── exporters/
│   │   │   ├── to_dxf.py
│   │   │   ├── to_json.py
│   │   │   └── to_sketchup.py
│   │   └── automations/
│   │       ├── auto_redraw_room.py
│   │       ├── auto_redraw_elevations.py
│   │       ├── auto_cabinet_place.py
│   │       └── cv_scene_validator.py
│   │
│   ├── contracts/                # RC-80-01, RC-40-01/05 stuff
│   │   ├── contract_model.py
│   │   ├── contract_generator.py
│   │   ├── billing_calculator.py
│   │   └── templates/            # Word/Markdown "contract base" files
│   │
│   ├── email/                    # RC-90-C templates
│   │   ├── email_renderer.py     # Fill {Job#}, {Client}, etc.
│   │   ├── email_templates.yaml  # Canonical text for all templates
│   │   └── email_batch_tools.py
│   │
│   ├── scheduling/               # RC-40-02, back-plan schedule
│   │   ├── backplan_engine.py
│   │   ├── capacity_model.py
│   │   └── client_timeline_export.py
│   │
│   ├── install/                  # RC-50-01/02, RC-90-D/E/F
│   │   ├── site_readiness_checker.py
│   │   ├── install_packet_builder.py
│   │   └── photo_naming_helper.py
│   │
│   └── warranty/                 # warranty intake + CoQ tracking
│       ├── warranty_intake_parser.py
│       ├── service_ticket_model.py
│       └── warranty_email_flows.py
│
├── apps/
│   ├── cli/
│   │   ├── cli.py                # Simple "choose a tool" CLI front end
│   │   └── commands/             # click/typer commands like `intake new`, `contract gen`
│   └── web/
│       └── (future)              # Streamlit/FastAPI frontends if you want
│
├── config/
│   ├── paths.yaml                # UNC paths, CV exports, contract template paths, etc.
│   ├── email_profiles.yaml       # Default "from" addresses, signatures
│   └── rates.yaml                # Labor/material rates for estimates/contracts
│
├── data_samples/
│   ├── intake_samples/
│   ├── spec_sheet_samples/
│   ├── cv_exports/
│   └── contracts/
│
└── tests/
    ├── test_intake.py
    ├── test_decisions.py
    ├── test_cv_parsers.py
    ├── test_contracts.py
    └── test_email.py

## Running the Trim Web App

Install:

pip install fastapi uvicorn pydantic typer pandas openpyxl

Run:

uvicorn apps.web.trim_api:app --reload --host 0.0.0.0 --port 8000

On computer:

http://localhost:8000

On phone (same Wi-Fi):

http://YOUR-PC-IP:8000

## Deploying to Render

1. Push this repository to GitHub.

2. In Render, create a new Web Service and connect it to the GitHub repo.

3. Render will detect `render.yaml` and configure the service automatically.

4. Ensure the build command is `pip install -r requirements.txt`.

5. Ensure the start command is `uvicorn apps.web.trim_api:app --host 0.0.0.0 --port $PORT`.

6. After deployment, Render will give you a public URL you can share with contractors. They can open it in a mobile browser and add it to their home screen.

