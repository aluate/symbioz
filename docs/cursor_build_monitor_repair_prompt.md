# 🧠 CURSOR PROMPT — Build Monitor / Repair / Redeploy Loop

**(Vercel + Render, GitHub-connected)**

---

You are acting as the build-monitor and repair agent for this repo.

## CONTEXT

- Repo: aluate/symbioz
- Two deploy targets:
  1) Symbioz web → Vercel (Root: apps/symbioz-web)
  2) Otto API → Render (Root: apps/otto, Docker runtime)
- Both Vercel and Render are connected to GitHub and auto-deploy on push.
- Current state: BOTH services have failed builds.
- Your job is to loop until BOTH deploy targets are GREEN.

## CRITICAL RULES

- Do NOT add features.
- Do NOT refactor unrelated code.
- Do NOT change infra unless required to fix a build.
- Fix ONE failure at a time.
- Every change must be justified by a concrete build error.
- Commit after each successful fix cycle.

---

## PHASE 1 — Collect failure signals (no assumptions)

### 1) Inspect Vercel failure:

- Identify latest failed deployment
- Capture:
  - build command used
  - exact error output
  - which step failed (install, build, postbuild, runtime)
  - whether it is path-related, dependency-related, or config-related

### 2) Inspect Render failure:

- Identify latest failed deploy
- Capture:
  - build logs
  - whether failure is during Docker build or container start
  - missing files, wrong workdir, or PORT issues

**Write findings to:** `docs/deploy_failures_latest.md`

---

## PHASE 2 — Classify failures

For EACH target, classify the failure as one of:

- PATH / ROOT DIRECTORY error
- PACKAGE MANAGER mismatch
- MISSING FILE (package.json, requirements.txt, etc.)
- ENV VAR missing
- BUILD COMMAND incorrect
- RUNTIME START command incorrect
- TYPESCRIPT / BUILD error
- DOCKER context / copy error

If classification is unclear, STOP and report.

---

## PHASE 3 — Repair (minimal change only)

### If Vercel failed:

- Verify:
  - Root Directory = apps/symbioz-web
  - package.json exists in that directory
  - build script uses `npx next build`
- Fix ONLY what the error requires.
- Do NOT touch Otto files unless required.

### If Render failed:

- Verify:
  - Root Directory = apps/otto
  - Dockerfile path is correct
  - Dockerfile copies correct files
  - Start command respects `$PORT`
- Fix ONLY what the error requires.
- Do NOT touch Symbioz web files unless required.

---

## PHASE 4 — Commit + redeploy

After fixing ONE failure:

1) Commit with message:
   "Fix: <short description of build failure>"

2) Push to origin/main

3) Wait for redeploy to trigger

4) Re-check build status for that target

---

## PHASE 5 — Loop

- If one target is GREEN and the other is still RED:
  → repeat PHASES 1–4 for the remaining failure.
- If BOTH are GREEN:
  → STOP.

---

## FINAL OUTPUT REQUIRED

- Summary of:
  - Root cause for Vercel failure
  - Root cause for Render failure
- Commits applied (hash + reason)
- Confirmation that:
  - Symbioz web is live on Vercel
  - Otto API is live on Render
- Any remaining WARNINGS (non-blocking)

---

## Notes

- This prompt recreates the Otto-style monitor/repair/redeploy loop *without* Otto running locally.
- Cursor acts as the executor.
- Forces reading real logs instead of guessing.
- Prevents "fix everything" refactors.
- Works even though Otto isn't running locally.

