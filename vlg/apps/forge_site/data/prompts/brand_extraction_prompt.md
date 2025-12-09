# Brand Extraction Prompt — For Otto/Cursor

**Purpose:** This prompt guides Otto/Cursor through extracting brand information from raw verbal or written input for Forge Site clients.

**Reference:** See `control/CONTROL_FS_BRANDING_GENERATION.md` for complete protocol.

**Usage:** Use this prompt when processing client input (transcripts, notes, conversations) to generate brand systems.

---

## Instructions for Otto/Cursor

You are extracting brand information from client input to generate a complete brand system for Forge Site.

**Your task:**
1. Read the client input (transcript, notes, conversation, email)
2. Extract all available information using the 10 input categories below
3. Fill gaps with reasonable inference where possible
4. Ask concise, batched questions only for critical missing information
5. Generate a complete brand system following `CONTROL_FS_BRANDING_GENERATION.md`

---

## Extraction Checklist

### 1. Business Context
- [ ] What they sell (product/service)
- [ ] Problem they solve
- [ ] Competitors (direct/indirect)
- [ ] Unique value proposition
- [ ] Market scope (local/regional/national)

**Extraction questions:**
- What is the core product or service?
- What problem does this solve for customers?
- Who else does something similar?
- What makes this different or better?

### 2. Audience
- [ ] Demographics (age, income, location if mentioned)
- [ ] Cultural/lifestyle identity
- [ ] Primary pain points
- [ ] Core values
- [ ] Industry/language norms
- [ ] Emotional triggers
- [ ] Psychographics

**Extraction questions:**
- Who is the ideal customer?
- What do they care about?
- What problems do they have?
- What motivates them?

### 3. Brand Energy
- [ ] 3–7 descriptive adjectives
- [ ] "Feels like…" metaphors
- [ ] "Never be…" constraints

**Extraction questions:**
- If this brand were a person, what three words describe them?
- What should the brand feel like?
- What should it never feel like?

### 4. Founder Voice
- [ ] Tone level (casual/formal)
- [ ] Style (poetic/direct, luxury/scrappy)
- [ ] Personality markers (weird, witty, serious, etc.)
- [ ] Industry language patterns
- [ ] Sentence structure and cadence

**Extraction method:**
- Analyze input text for:
  - Sentence length (short/medium/long)
  - Word choice (simple/complex, technical/colloquial)
  - Formality level
  - Metaphors used
  - Emotional tone

### 5. Core Philosophy
- [ ] What they stand for
- [ ] What they reject
- [ ] The "why" behind the product/service
- [ ] Worldview that drives decisions

**Extraction questions:**
- What do you believe in?
- What drives you to do this work?
- What's wrong with how things are done now?

### 6. Market Position
- [ ] Premium or affordable
- [ ] Performance or simplicity
- [ ] Traditional or futuristic
- [ ] Local or global
- [ ] Boutique or mass market

**Infer from:**
- Pricing language
- Target customer descriptions
- Competitive positioning
- Value proposition statements

### 7. Aesthetic Preferences
- [ ] Shapes (geometric/biomorphic/angular)
- [ ] Motifs (mountain, bee, flame, etc.)
- [ ] Interior design styles
- [ ] Architectural references
- [ ] Material feel (wood, steel, etc.)
- [ ] Dark or light world (mood)

**Extraction questions:**
- Any design references you love?
- What visual style appeals to you?
- How should the brand look and feel?

### 8. Color Psychology
- [ ] Preferred palettes (if mentioned)
- [ ] Emotional intent
- [ ] Colors to avoid
- [ ] Industry color conventions

**Extraction questions:**
- Any colors you love or hate?
- What should your brand colors communicate?

### 9. Symbolic Themes
- [ ] Archetypes
- [ ] Mythological sources
- [ ] Visual metaphors
- [ ] Biological or industrial motifs

**Infer from:**
- Business type
- Archetype patterns
- Visual metaphors in language

### 10. Non-Negotiables
- [ ] Must include (required elements)
- [ ] Must never use (forbidden words/colors/styles)
- [ ] Legal requirements
- [ ] Cultural sensitivities

**Extraction questions:**
- Anything that absolutely must be included?
- Anything that must never be used?

---

## Extraction Workflow

### Step 1: Read Input
- Identify input source (transcript, notes, form, email)
- Note context and completeness
- Flag obvious gaps

### Step 2: Extract Available Information
- Go through each of the 10 categories
- Extract explicit information
- Note implied information
- Mark missing categories

### Step 3: Make Reasonable Inferences
**When to infer:**
- Industry has standard patterns (e.g., builders → earthy colors, solid typography)
- Business type suggests archetype (e.g., creative agency → Creator)
- Founder voice can be inferred from writing style
- Market position can be inferred from pricing/value prop

**When NOT to infer:**
- Specific color preferences
- Exact brand energy adjectives
- Non-negotiables
- Critical missing business context

### Step 4: Ask Targeted Questions (If Needed)
**Only ask if:**
- Critical information is missing (business context, audience)
- Cannot reasonably infer (specific preferences, non-negotiables)

**Batch questions:**
- Group related questions together
- Use open-ended questions when possible
- Provide examples to guide answers

**Example batched questions:**
> "I need a few details to complete your brand system:
> 
> 1. Who is your ideal customer? (What do they care about? What problems do they have?)
> 
> 2. What should your brand feel like? (3 words, plus what it should never feel like)
> 
> 3. Any colors, words, or styles you love or hate?"

### Step 5: Generate Brand System
- Follow `CONTROL_FS_BRANDING_GENERATION.md` section 2-9
- Populate all required sections
- Create complete deliverable bundle
- Flag any assumptions made

---

## Output Format

Generate structured data and documentation:

**1. Structured Data (JSON):**
```json
{
  "extractedInputs": {
    "businessContext": { ... },
    "audience": { ... },
    "brandEnergy": { ... },
    "founderVoice": { ... },
    "corePhilosophy": { ... },
    "marketPosition": { ... },
    "aestheticPreferences": { ... },
    "colorPsychology": { ... },
    "symbolicThemes": { ... },
    "nonNegotiables": { ... }
  },
  "assumptions": [
    "Inferred earthy color palette from construction industry",
    "Inferred Creator archetype from custom work focus"
  ],
  "missingInformation": [
    "Specific color preferences",
    "Logo direction preferences"
  ]
}
```

**2. Brand System Files:**
- Follow deliverable bundle structure (section 10 of control doc)
- Create all required files
- Use consistent naming conventions

---

## Common Patterns

### Construction/Trades
**Typical inferences:**
- Earthy, grounded color palettes (steel, rust, charcoal)
- Solid, reliable typography (Inter, System fonts)
- Creator + Engineer archetype blend
- Direct, no-nonsense voice
- Craftsmanship themes

### Creative Services
**Typical inferences:**
- More varied color palettes (often bolder)
- Creative typography (more expressive fonts)
- Creator archetype
- More personality in voice
- Innovation themes

### Professional Services
**Typical inferences:**
- Professional, trustworthy colors (blues, grays)
- Clean, readable typography
- Sage or Caregiver archetype
- Professional but approachable voice
- Trust and expertise themes

### Product/Retail
**Typical inferences:**
- Brand-aligned colors (may vary widely)
- Product-focused messaging
- Merchant archetype
- Clear, benefit-focused voice
- Quality and value themes

---

## Quality Checklist

Before finalizing extraction:
- [ ] All 10 input categories addressed (even if inferred)
- [ ] Assumptions clearly documented
- [ ] Missing information noted
- [ ] Brand system complete and consistent
- [ ] Output follows control doc structure
- [ ] Brand tokens ready for Forge Site build

---

**End of Prompt**

Use this prompt when processing client input for brand generation. Reference `CONTROL_FS_BRANDING_GENERATION.md` for complete protocol.

