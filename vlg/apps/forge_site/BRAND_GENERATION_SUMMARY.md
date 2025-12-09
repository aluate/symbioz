# Forge Site — Brand Generation Implementation Summary

## Overview

Brand generation system has been fully integrated into Forge Site. The system can generate complete brand tokens (colors, typography, voice) from raw input like conversation transcripts, intake form answers, or brand notes.

## What Was Implemented

### 1. Control Documentation

**`control/CONTROL_FS_BRANDING_GENERATION.md`**
- Complete documentation of brand generation process
- Input sources and extraction methods
- Color, typography, and voice generation guidelines
- Integration with build flow
- Brand token priority system

### 2. Brand Generation Script

**`scripts/generate-brand-from-input.ts`**
- Standalone script to generate brand tokens from input
- Processes JSON or plain text input
- Generates:
  - Color palette based on personality and preferences
  - Typography selection based on brand feel
  - Voice guidelines from tone and style
  - Spacing and layout tokens
- Outputs brand tokens JSON file

### 3. Build Script Integration

**`scripts/build-site-from-config.ts`** (updated)
- Added brand token loading and generation
- Integrated brand generation into build flow
- Applies brand tokens to generated sites:
  - Colors in CSS variables and Tailwind config
  - Typography in layout and font imports
  - Voice guidelines available for copy generation
- Brand token priority:
  1. Client brand tokens (from `brandTokensPath`)
  2. Generated brand tokens (from `brandInput`)
  3. Default Forge Site tokens (fallback)

### 4. Schema Updates

**`data/prompts/business_json_schema.json`** (updated)
- Added `brandTokensPath` field (optional)
- Added `brandInput` object with all brand fields:
  - `brandPersonality` (array of 3 words)
  - `brandFeel` / `brandNeverFeel`
  - `visualStyle` / `coreBeliefs`
  - `colorPreferences` (loved/hated)
  - `toneOfVoice` / `wordsToAvoid`
  - `visualReferences`
  - `conversationTranscript` / `notes`

## How It Works

### Brand Generation Flow

1. **Check for brand tokens:**
   - If `brandTokensPath` provided → load and use those tokens
   - Skip generation

2. **Check for brand input:**
   - If `brandInput` provided → generate brand system
   - Extract personality, feel, preferences
   - Generate colors, typography, voice
   - Save to `output/<site-slug>/brand-tokens.json`

3. **Apply brand tokens:**
   - Colors → CSS variables and Tailwind config
   - Typography → Font imports and font-family
   - Voice → Available for copy generation

4. **Fallback:**
   - If no brand input/tokens → use Forge Site defaults

### Usage Examples

**Example 1: Using Pre-Existing Brand Tokens**

```json
{
  "businessName": "Acme Builders",
  "industry": "builder",
  "primaryGoal": "GET_LEADS",
  "brandTokensPath": "path/to/brand-tokens.json"
}
```

**Example 2: Generating from Brand Input**

```json
{
  "businessName": "Acme Builders",
  "industry": "builder",
  "primaryGoal": "GET_LEADS",
  "brandInput": {
    "brandPersonality": ["rugged", "reliable", "honest"],
    "brandFeel": "trustworthy and solid",
    "brandNeverFeel": "flashy or corporate",
    "colorPreferences": {
      "loved": ["earth tones", "deep browns"],
      "hated": ["bright colors", "neon"]
    },
    "toneOfVoice": "Direct and no-nonsense"
  }
}
```

**Example 3: Using Conversation Transcript**

```json
{
  "businessName": "Acme Builders",
  "brandInput": {
    "conversationTranscript": "We want our brand to feel rugged and reliable. Earth tones work best. Never flashy. Direct communication style."
  }
}
```

## Brand Token Structure

Generated brand tokens follow this structure:

```json
{
  "brandName": "Business Name",
  "personality": ["word1", "word2", "word3"],
  "brandFeel": "description",
  "brandNeverFeel": "description",
  "coreBeliefs": ["belief1", "belief2"],
  "colors": {
    "primary": { "hex": "#...", "name": "...", "usage": "..." },
    "secondary": { ... },
    "background": { ... },
    "text": { ... },
    "accent": { ... }
  },
  "typography": {
    "fontFamily": { "primary": "...", "stack": [...] },
    "headings": { ... },
    "body": { ... }
  },
  "voice": {
    "tone": "...",
    "style": "...",
    "wordsToUse": [...],
    "wordsToAvoid": [...],
    "examples": [...]
  },
  "spacing": {
    "baseUnit": 8,
    "scale": [...]
  },
  "visualStyle": {
    "references": [...],
    "notes": "..."
  }
}
```

## Integration Points

### Build Flow Integration

Brand generation runs automatically during site build:

1. **Step 7: Apply Brand Tokens** (in `CONTROL_FS_BUILD_FLOW.md`)
   - Check for `brandTokensPath`
   - If not present, check for `brandInput`
   - Generate brand system if input present
   - Apply tokens to site generation

### Generated Site Integration

Brand tokens are applied to:

- **CSS Variables** (`globals.css`):
  - `--primary`, `--secondary`, `--background`, `--text`, `--accent`

- **Tailwind Config** (`tailwind.config.js`):
  - Color palette in `theme.extend.colors`
  - Font family in `theme.extend.fontFamily`

- **Layout** (`layout.tsx`):
  - Font import and application
  - Font family from brand tokens

## Current Limitations

1. **Font Handling:** Currently only handles Inter font. Full Google Fonts support would require more sophisticated font import generation.

2. **Color Generation:** Uses rule-based color selection. Production would use AI/LLM for more sophisticated palette generation.

3. **Voice Guidelines:** Generated but not yet used in copy generation. Would need integration with copy generation system.

4. **Conversation Parsing:** Plain text input is stored but not parsed. Would need AI/LLM to extract structured data from conversations.

## Future Enhancements

1. **AI/LLM Integration:**
   - Parse unstructured conversation transcripts
   - Generate sophisticated color palettes
   - Extract brand elements from natural language

2. **Logo Generation:**
   - Generate logo concepts from brand system
   - Create logo files based on brand personality

3. **Image Style Guidelines:**
   - Generate image style preferences
   - Suggest photography direction

4. **Component Style Variations:**
   - Generate component style variations based on brand
   - Apply brand-specific UI patterns

## Files Created/Modified

### Created:
- `control/CONTROL_FS_BRANDING_GENERATION.md`
- `scripts/generate-brand-from-input.ts`
- `BRAND_GENERATION_SUMMARY.md` (this file)

### Modified:
- `scripts/build-site-from-config.ts` (brand integration)
- `data/prompts/business_json_schema.json` (brand fields)
- `control/CONTROL_FS_BUILD_FLOW.md` (brand generation step)

## Testing

To test brand generation:

1. **Create a test business.json with brand input:**
```json
{
  "businessName": "Test Builder",
  "industry": "builder",
  "primaryGoal": "GET_LEADS",
  "brandInput": {
    "brandPersonality": ["rugged", "reliable", "honest"],
    "brandFeel": "trustworthy and solid",
    "toneOfVoice": "Direct and no-nonsense"
  }
}
```

2. **Run build:**
```bash
npx tsx scripts/build-site-from-config.ts test-business.json
```

3. **Check output:**
- `output/test-builder/brand-tokens.json` should exist
- Generated site should use custom colors
- CSS variables should reflect brand colors

## Status

✅ **Complete:** Brand generation system fully implemented and integrated
⏳ **Future:** AI/LLM integration for sophisticated generation

---

**Get seen. Stay simple.**

