
# How to Use This Document
This file is your **permanent, universal control system** for generating Cursor instructions using ChatGPT. Save it somewhere safe.

Whenever you start a new Cursor task, follow this process:

1. **Open a fresh Cursor chat.**
2. Paste the *goal* only (e.g., "Add a logging module", "Fix UI bug", "Add authentication").
3. Ask ChatGPT: **"Create a Cursor control doc for this task."**
4. ChatGPT will read this document and produce:
   - a fully structured, safe, incremental, Cursor-ready prompt
   - with task phases
   - with file targeting
   - with PROJECT_LOG.md updates
   - with safety/unambiguous execution rules
5. Paste the generated control doc into Cursor.
6. Let Cursor run.

If Cursor context gets high (70–80%), or if the chat gets messy:
- Start a new Cursor chat
- Paste the goal again
- Repeat steps above

This process ensures you'll **never lose control of your repo** and **never depend on ChatGPT's memory**.

---

# ChatGPT → Cursor Control Document (Refactored Universal Edition)

This is the **master specification** for how ChatGPT will generate instructions, control documents, and task lists for Cursor across *any* project, language, framework, or repository.  
It is refactored to be:
- Concise
- Ordered logically
- Universal (technology-agnostic)
- Non-redundant
- Explicit and enforceable
- Safe for long-lived repositories

This is the rulebook ChatGPT will follow every time it generates a Cursor prompt.

---

# 1. Core Execution Principles

1. **Cursor has no long-term memory.**  
   Treat the repo + PROJECT_LOG.md as the single source of truth.

2. **Tasks must be completed in strict sequential order.**

3. **Cursor must not ask mid-task questions.**  
   If information is missing AND cannot be inferred from the repo, Cursor must stop and report what is missing.

4. **Efficiency and safety override creativity.**

5. **Prompts must stay compact** and avoid unnecessary explanation.

---

# 2. Required Opening for Every Cursor Prompt
Every Cursor instruction produced by ChatGPT must begin with:
```
Use the existing repository files and PROJECT_LOG.md as the source of truth.
Work in Auto mode.
Do not ask for clarification.
Do not load entire files unless necessary.
Only modify the files explicitly listed in the tasks.
Complete each task in order.
Update PROJECT_LOG.md after each major task.
```

---

# 3. Required Ending for Every Cursor Prompt
Every Cursor instruction must end with:
```
When finished:
- Summarize changes made
- Update PROJECT_LOG.md
- Append a new entry to Version History
Do not ask for further instructions.
```

---

# 4. Repo Discovery & Environment Detection
Cursor must:
- Detect project structure automatically (single repo, monorepo, multi-service).
- Detect languages and frameworks by scanning file extensions + config files.
- Detect dependency management systems minimally.
- Detect runtime environments (Node, Python, Go, Docker, serverless, JVM, etc.).
- Never assume or guess the technology stack.

ChatGPT must tailor all instructions to the detected stack.

---

# 5. File Targeting & Modification Rules
1. **Explicit file targeting is mandatory.**  
   Cursor may *only* modify files explicitly listed.

2. **No architecture changes unless explicitly authorized.**
   - No renaming
   - No refactoring
   - No reorganizing folders
   - No deleting components

3. **Safe insertion is preferred over rewriting.**
   - Use anchors or markers for placement.

4. **Full file rewrites are forbidden** unless explicitly authorized AND file < 300 lines.

5. **Never modify lockfiles** unless explicitly instructed.

6. **Preserve comments, formatting, and structure.**

---

# 6. PROJECT_LOG.md Protocol (Mandatory)
Cursor must:
- Update the log after each major task.
- Use append-only behavior.
- Never rewrite or delete previous entries.
- Maintain sections:
  - Project Structure Summary
  - Completed Tasks
  - In-Progress Tasks
  - TODO / Upcoming Tasks
  - Assumptions Made
  - Notes for Future Sessions
  - Version History

This file serves as the project’s **stateful memory**.

---

# 7. Task Design Rules
1. Break work into **small, coherent phases**.
2. Use action verbs: Create, Modify, Insert, Validate, Connect.
3. Include fallbacks: missing file → soft fail; bad schema → error message.
4. Keep tasks technology-agnostic unless dictated by the repo.

---

# 8. Safety & Failure Handling
Cursor must:
- Stop immediately if destructive behavior is attempted.
- Report suspicious rewrites.
- Never fix issues by modifying multiple files unintentionally.
- Never remove code automatically.
- Provide human-readable errors.

If a task cannot be completed: Cursor must halt and explain.

---

# 9. Context Management & Reset Rules
- If context > 75%: finish current task and stop.
- Next phase must be run in a new chat.
- User reseeds ChatGPT with:
  - The goal
  - This control document
  - PROJECT_LOG.md

Cursor must never continue new tasks at high context.

---

# 10. Large Task Chunking Protocol
For complex or multi-file work:
1. Divide into phases.
2. Each phase modifies at most 1–3 files.
3. User starts next phase manually.

---

# 11. When-In-Doubt Rule
If a requirement is ambiguous AND cannot be inferred from:
- Repo structure
- PROJECT_LOG.md
- Prompt

Cursor must **stop** and report instead of guessing.

---

# 12. Specialized Modules
### 12.1 APIs
- Modify only target controllers.
- Require schema validation.
- Provide API docs.
- Update integration tests.

### 12.2 Frontend
- Respect component architecture.
- Do not modify routing/layout without permission.
- Keep UI/style changes scoped.

### 12.3 Data Pipelines
- Require strict schemas.
- Enforce idempotency.
- Implement logging.

### 12.4 Testing
- Place tests under tests/.
- Mirror source structure.
- Use mocks for external systems.

### 12.5 Infrastructure
- Target only specified Terraform/Pulumi modules.
- Avoid rewriting stateful files.

### 12.6 CI/CD
- Edit minimal YAML.
- Do not break step order.
- Never include secrets.

### 12.7 Documentation
- Update README/docs.
- Document new commands or flows.

---

# 13. Cross-Project Reusability
This document must:
- Apply to all stacks
- Scale to any repo size
- Remain framework-agnostic
- Never reference project-specific context

---

# End of ChatGPT → Cursor Control Document (Refactored Universal Edition)
