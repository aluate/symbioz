# Otto - Persistent AI Agent

**Status:** Phase 1 - Core Skeleton + API Server  
**Purpose:** Provider-agnostic AI agent that lives with your files

## Overview

Otto is a persistent AI agent designed to:
- Live with your files (repos, Google Drive, local storage)
- Work independently of external AI tools (ChatGPT, Cursor)
- Execute tasks, organize outputs, propose improvements
- Integrate with Life OS for task management
- **NEW:** Accept prompts from anywhere via HTTP API

## Architecture

```
apps/otto/
├── otto/
│   ├── core/          # Core models, runner, health checks
│   ├── skills/        # Individual skills (repo_lister, repo_audit)
│   ├── api.py         # HTTP API server (NEW)
│   ├── config.py      # Configuration loader
│   └── cli.py         # CLI entry point
├── otto_config.yaml   # Configuration file
├── pyproject.toml     # Project configuration
└── README.md
```

## Installation

```bash
cd apps/otto
pip install -r requirements.txt
# Or: pip install -e .
```

## Usage

### CLI Commands

#### Run a sample task
```bash
otto run-sample
```
Lists the repository structure and writes to `reports/repo_tree_sample.md`

#### Run health checks
```bash
otto health
```
Checks all skills for issues

#### Run repo audit
```bash
otto audit
```
Audits the Otto repository and writes report to `reports/audits/`

#### Start API Server (NEW)
```bash
otto server
# Or with custom host/port:
otto server --host 0.0.0.0 --port 8001
```

### HTTP API (NEW)

Otto now has an HTTP API server that accepts prompts from anywhere!

#### Start the server:
```bash
otto server
```

#### Endpoints:

**POST /prompt** - Send a text prompt to Otto
```json
{
  "prompt": "List the repository structure",
  "task_type": "repo_list",
  "payload": {}
}
```

**POST /task** - Send a structured task
```json
{
  "type": "repo_list",
  "payload": {
    "target_repo": ".",
    "output_path": "reports/tree.md"
  }
}
```

**GET /skills** - List available skills

**GET /health** - Health check

**GET /** - API info

#### Example with curl:
```bash
curl -X POST http://localhost:8001/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Audit the Otto repository"}'
```

## Configuration

Edit `otto_config.yaml` to configure:
- Default repository root
- Reports directory
- Safety settings (auto-apply repairs, etc.)

## Skills

### RepoListerSkill
Lists repository structure and writes to Markdown file.

### RepoAuditSkill
Audits the Otto repository for:
- Empty directories
- Large files
- Missing __init__.py files
- Other structural issues

## Integration with Life OS

Life OS can send prompts to Otto via the API. See `apps/life_os/` for the web interface.

## Development Status

**Phase 1 (Current):** Core skeleton with basic skills + HTTP API  
**Phase 2 (Planned):** LLM abstraction, Google Drive integration  
**Phase 3 (Planned):** Advanced prompt processing, Life OS deep integration

## Safety

- All changes are proposal-based by default
- No auto-apply unless explicitly configured
- All actions are logged
- Reversible via git
