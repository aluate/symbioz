# ForgeSite Build — Website Factory Rebrand Control

## Goal

Rebrand **ForgeSite Build** from a generic "web services" vibe into a **Website Factory**:

- We are **not** an agency.
- We are a **system that produces websites** in a predictable, repeatable way.
- We serve **builders, trades, and shops**.
- Ongoing support exists, but is **structured and limited**, not endless tweaks.

Cursor: follow the phases below in order. After each phase, log:

`[FACTORY_REBRAND] Phase X complete`

---

## Global Tone & Language Guidelines

### Emphasize

- **Factory language**: system, production line, modules, passes, runs, factory, line, output.
- **Speed & reliability**: built in days, predictable, repeatable, low-drama.
- **Niche**: builders, trades, shops, steel buildings, cabinet shops, etc.
- **Done-for-you**: we build the site from intake; client doesn't design.

### Avoid

- "Agency", "studio", "freelancer", "designer" for our role.
- "Custom web design", "bespoke design", "pixel-perfect tweaks".
- Language that suggests unlimited revisions or open-ended creative work.

### Phrase Replacement Map

Apply these replacements repo-wide where appropriate:

- `web services` → `website factory system`
- `our web services` → `our website factory`
- `our services` (when referring to web) → `our website factory packages`
- `web design` → `factory-built websites`
- `custom web design` → `factory-built website tailored from your intake`
- `agency` / `our agency` → `our website factory`
- `design revisions` → `factory passes`
- `tweaks` / `small tweaks` → `config changes`
- `project` (when referring to a site build) → `factory run` or `build cycle`
- `maintenance` → `support plan` or `factory support plan`

If a replacement makes a sentence awkward, rewrite the sentence to keep the **factory** framing and the **done-for-you** nature.

---

## Phase 1 – Marketing Copy Overhaul

### Files

- `app/(marketing)/page.tsx`
- `app/layout.tsx`
- `BRAND_GUIDE.md`

#### 1.1 Hero Section (page.tsx)

**Target outcome:**

- Brand: **ForgeSite Build**
- Primary headline options (pick 1, or minor variants):

  - "Website Factory for Builders, Trades & Shops"

  - "Professional Websites, Built by a Website Factory for the Trades"

  - "AI-Assisted Website Factory for Builders and Shops"

- Subheadline example:

  > "You give us your info. Our system builds your site in days—no endless meetings, no agency drama."

- Primary CTA text:

  - "Get a Website Plan"
- Secondary CTA text:

  - "See Example Factory Output"

#### 1.2 Sections

Update sections so they reflect the factory model. Suggested structure and copy direction:

1. **Who We Build For**

   Short heading: "Built for the Trades"

   Bullet cards: Home Builders, Remodelers, Cabinet Shops, Steel Buildings, Specialty Trades.

2. **How the Website Factory Works**

   3–4 steps:

   1. Intake  
      > "Fill out a structured intake (or talk with our bot)."
   2. Factory Run  
      > "Our modules, copy system, and layout engine assemble your site."
   3. Review  
      > "You review the preview and request small config changes."
   4. Launch  
      > "We launch, connect your domain, and you're live."

3. **Packages**

   Rename to **"Factory Packages"**.

   Example names (you can tweak):

   - **Starter Run** – for small trades  
   - **Workhorse Run** – for established builders/shops  
   - **Premium Run** – for multi-location or high-end firms  

   Each package description must emphasize:

   - defined page count
   - defined module set
   - lead capture
   - timeline ("most sites in 3–7 days after intake")

4. **Why a Website Factory (vs. Agency)**

   Add a small comparison list:

   - No endless revision cycles  
   - No vague hourly billing  
   - Built from proven modules  
   - Designed specifically for the construction world  

5. **FAQ**

   Include at least:

   - "Are you a web design agency?"  
     > "No. We're a website factory. We use proven layouts and modules to build sites fast instead of designing from scratch."
   - "Can I get custom design work?"  
     > Only via a scoped upgrade / new factory pass (no open-ended tweaks).
   - "How many revisions do I get?"  
     > Clarify that small **config changes** are allowed; large redesigns require a new factory run.

#### 1.3 Meta Description (app/layout.tsx)

Update to something like:

> "ForgeSite Build is a website factory for builders, trades, and shops. We turn your intake into a professional, lead-ready website in days—not weeks."

#### 1.4 Brand Guide (BRAND_GUIDE.md)

Add/update sections to explicitly mention:

- "We are a website factory, not an agency."
- Core values: speed, clarity, system, respect for trades' time.
- "Support exists through structured plans and bot-driven config changes, not endless custom design."

Log:  
`[FACTORY_REBRAND] Phase 1 complete`

---

## Phase 2 – Intake & Forms

### Files

- `app/intake/page.tsx`
- `app/intake/success/page.tsx`

#### 2.1 Intake Page

- Heading: "Start a Website Factory Run"
- Subtext: "Answer a few focused questions about your business. We use this intake to assemble your site from factory-tested modules."
- Field helper texts should reinforce:

  - we're not asking for design opinions
  - we're collecting facts about their work, clients, and jobs

Example helper:

- For services:  
  > "List the main services you actually sell. We'll turn this into clear sections on your site."

#### 2.2 Success Page

- Message example:

  > "Your website factory run has been queued.  
  > We'll review your intake, generate a plan, and send a proposal outlining your build and launch timeline."

- Add note about typical timeline: "Most sites go live within 3–7 days of intake approval and payment."

Log:  
`[FACTORY_REBRAND] Phase 2 complete`

---

## Phase 3 – Proposal Template (Factory Focus)

### Files

- `factory/proposal/generateProposal.ts` (or current proposal generator path)
- `PRICING_MODEL.md`

#### 3.1 Proposal Generator

Adjust proposal sections to:

1. **Overview**

   - Introduce ForgeSite Build as a "website factory for builders, trades & shops."
   - Mention the specific **Factory Package** recommended.

2. **Factory Run Plan**

   - Show pages and modules as "Factory Output" not "custom design."
   - Example language:  
     > "Your site will be assembled from proven modules: Hero, Services Grid, Project Gallery, Testimonials, Contact & Lead Capture."

3. **Timeline**

   - "Most factory runs complete in 3–7 days after intake confirmation and payment."

4. **Support**

   - Describe support plan as **Factory Support Plan** with:

     - small config changes
     - uptime checks
     - analytics
     - NO open-ended redesigns

5. **Scope Guardrails**

   - Explicitly state:

     > "Major layout or design changes after launch require a new factory run or upgrade, not free revisions."

#### 3.2 Pricing Model

- Rename any "hourly" framing to **packages** and **support plans**.
- Make sure the document describes:

  - base package fees
  - optional add-ons
  - monthly support tiers
  - no "unlimited revision" language

Log:  
`[FACTORY_REBRAND] Phase 3 complete`

---

## Phase 4 – Chat Bot Persona (Factory Assistant)

### Files

- `app/api/chat/route.ts`
- `factory/bot/BOT_PERSONA.md` (create if not present)

#### 4.1 Persona Spec (BOT_PERSONA.md)

Bot name suggestion: **Forge Assistant** or **Factory Assistant**.

**Role:**

- Intake helper and config editor for the website factory.
- Not a general consultant; keeps scope tight.

**Personality:**

- Direct, respectful, trades-friendly.
- Plain language, no jargon.
- Time-conscious: keeps conversations short and focused.

**Capabilities:**

- Ask follow-up questions to complete intake.
- Suggest appropriate Factory Package.
- Explain the factory process (intake → factory run → preview → launch).
- Trigger or propose small config changes (change text, swap images, update services list).
- Log requests for Otto/Cursor when they require code/config updates.

**Boundaries (must say NO to):**

- Full redesign requests ("Make it more artsy", "Try 5 layouts").
- Speculative strategy work not tied to the site.
- Free extra pages or modules outside the package.
- Anything outside website / intake / config context.

**Language examples:**

- "We're a website factory, so we work from proven layouts instead of designing from scratch."
- "That change is bigger than a config tweak. I can log it as a new factory run or upgrade for Karl to review."
- "Tell me what changed in your business—services, locations, or clients—and I'll update the site config."

#### 4.2 Chat Route

- Ensure responses reference **"website factory"** not "agency".
- When user asks for big changes, respond with:

  - explanation of scope  
  - offer to create a new factory run / upgrade.

Log:  
`[FACTORY_REBRAND] Phase 4 complete`

---

## Phase 5 – Documentation & Control Docs

### Files

- `CONTROL.md`
- `FORGESITE_BUILD_MASTER_PROMPT.md`
- `DATA_MODEL.md`
- `README.md`
- `ONBOARDING_CHECKLIST.md`

#### 5.1 CONTROL.md

- Update description of the system to:

  > "ForgeSite Build is a website factory for builders, trades & shops. Otto and Cursor work together to assemble sites from modular components based on structured intake data."

- Add a brief section:

  - "Factory Philosophy" (no bespoke work, standardized modules, config-driven).

#### 5.2 Master Prompt

- Ensure `FORGESITE_BUILD_MASTER_PROMPT.md`:

  - Uses the phrase **"website factory"** multiple times.
  - Describes phases as "factory runs" where relevant.
  - Mentions that automation should support **repeatable production**, not one-off design work.

#### 5.3 Data Model

- In `DATA_MODEL.md`, document modules explicitly as:

  - "Factory Modules"
  - part of the "Website Factory Library"

- Mention:

  > "Client sites are constructed by composing these factory modules according to the intake and package selected."

#### 5.4 README & Onboarding

- README intro:

  > "ForgeSite Build is a website factory that produces professional websites for builders, trades & shops."

- Onboarding checklist:

  - Frame client onboarding as "Queue a factory run" rather than "Start a web design project."

Log:  
`[FACTORY_REBRAND] Phase 5 complete`

---

## Phase 6 – Testing & Verification

### 6.1 Phrase Search

Global search the repo for these **banned or risky phrases** and either remove or rewrite:

- `web services`
- `web design services`
- `design agency`
- `agency`
- `our agency`
- `custom design`
- `unlimited revisions`
- `we'll tweak until you're happy`
- `we'll tailor everything to your taste`
- `designer` (when referring to us; allowed when referring to client's role)

Replace them with factory-framed alternatives per the map at the top.

### 6.2 Smoke Tests

- Run `npm run lint` and `npm run build`.
- Ensure marketing page builds with no type errors after text changes.
- Manually test:

  - marketing landing page
  - intake form submission
  - any existing proposal generation endpoints
  - chat endpoint (if wired)

### 6.3 Sanity Review Checklist

Confirm that everywhere a user interacts with us, they understand:

1. We are a **website factory**, not a general web agency.
2. There are **clear packages**, not open-ended time blocks.
3. Revisions = **config changes**; bigger changes require a new factory run.
4. Our niche is **builders, trades, and shops.**

Log final:

`[FACTORY_REBRAND] All phases complete`

---
