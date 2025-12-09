# Forge Site — Brand Generation Control

## Overview

Forge Site can generate a complete brand system from raw input: conversation transcripts, intake form answers, notes, or any text that describes the business's brand identity. This system extracts brand personality, visual direction, and values, then generates brand tokens (colors, typography, voice) that can be applied to the generated website.

## When Brand Generation Runs

Brand generation is triggered during the build flow when:

1. `business.json` includes `brandInput` field (raw text, conversation, notes)
2. `business.json` does NOT include `brandTokensPath` (pre-existing tokens)
3. Brand generation is explicitly requested

If `brandTokensPath` is provided, those tokens are used directly (no generation needed).

## Input Sources

Brand generation can process:

- **Conversation transcripts** - Client conversations about their brand
- **Intake form answers** - Responses to brand personality questions
- **Brand notes** - Written descriptions of brand identity
- **Mixed input** - Combination of the above

The system extracts:
- Brand personality (3 words)
- Brand feel / never feel
- Visual style preferences
- Core beliefs and values
- Color preferences (loved/hated)
- Tone of voice direction
- Visual references

## Brand Generation Process

### Step 1: Extract Brand Elements

Parse input to identify:

- **Personality Words** - 3 descriptive words
- **Brand Feel** - What it should feel like (e.g., "confident and warm")
- **Brand Never Feel** - What to avoid (e.g., "corporate," "flashy")
- **Visual Style** - Design references, aesthetic direction
- **Core Beliefs** - What drives the business
- **Color Preferences** - Colors loved, colors hated
- **Tone Direction** - Professional/friendly/casual/etc.
- **Words to Avoid** - Specific language to exclude

### Step 2: Generate Color Palette

Based on extracted preferences:

1. **Analyze color preferences:**
   - Colors mentioned (loved/hated)
   - Industry conventions
   - Brand personality alignment

2. **Generate palette:**
   - Primary color (main brand color)
   - Secondary color (supporting)
   - Background color (neutral, readable)
   - Text color (high contrast, readable)
   - Accent color (optional, for highlights)

3. **Ensure accessibility:**
   - WCAG contrast ratios
   - Readability on light/dark backgrounds
   - Color-blind friendly combinations

4. **Apply brand feel:**
   - Calm brands → muted, soft colors
   - Bold brands → saturated, high contrast
   - Professional → neutral with strategic accent

### Step 3: Generate Typography

Based on brand personality:

1. **Select font family:**
   - Professional/formal → serif or structured sans
   - Modern/clean → geometric sans
   - Friendly/approachable → humanist sans
   - Creative → display or unique sans

2. **Define typography scale:**
   - Heading sizes (H1-H4)
   - Body text size
   - Line heights
   - Font weights

3. **Match brand feel:**
   - Formal → traditional, structured
   - Modern → clean, minimal
   - Warm → rounded, approachable

### Step 4: Generate Voice Guidelines

Extract and codify:

1. **Tone descriptors:**
   - Professional but friendly
   - Casual and approachable
   - Direct and no-nonsense
   - Creative and playful

2. **Writing style:**
   - Sentence length preferences
   - Word choice (formal/casual)
   - Use of contractions
   - Technical vs. plain language

3. **Voice rules:**
   - Words to use
   - Words to avoid
   - Example phrases
   - Do's and don'ts

### Step 5: Generate Spacing & Layout Tokens

Based on brand personality:

- **Spacing scale** - 8px grid (default) or custom
- **Border radius** - Sharp (professional) vs. rounded (friendly)
- **Component spacing** - Tight (efficient) vs. generous (breathable)

### Step 6: Output Brand System

Generate JSON structure:

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

## Integration with Build Flow

1. **Check for brand input** in `business.json`
2. **Run brand generation** if input present
3. **Save brand tokens** to `output/<site-slug>/brand-tokens.json`
4. **Apply tokens** during site generation
5. **Reference tokens** in generated components

## Brand Token Priority

1. **Client brand tokens** (from `brandTokensPath`) - highest priority
2. **Generated brand tokens** (from brand generation) - second priority
3. **Default Forge Site tokens** - fallback

## AI/LLM Integration

Brand generation uses AI/LLM to:

- Parse unstructured input
- Extract brand elements
- Generate color palettes
- Suggest typography
- Codify voice guidelines

The system should:
- Use clear prompts
- Provide examples
- Validate outputs
- Handle edge cases

## Output Files

Generated brand system saved as:

- `output/<site-slug>/brand-tokens.json` - Full brand token JSON
- `output/<site-slug>/brand-system.md` - Human-readable brand guide (optional)

## Error Handling

- **No brand input:** Skip generation, use defaults
- **Unparseable input:** Log warning, use defaults
- **Invalid color generation:** Fall back to safe defaults
- **Missing personality:** Use industry defaults

## Usage

```bash
# Generate brand from input
npx tsx scripts/generate-brand-from-input.ts \
  --input "path/to/brand-input.txt" \
  --output "output/brand-tokens.json"

# Or integrated in build flow
npx tsx scripts/build-site-from-config.ts business.json
# (automatically runs brand generation if brandInput present)
```

## Brand Generation Prompts

The system uses structured prompts to extract brand elements:

1. **Personality Extraction:** "Extract 3 words that describe this brand's personality"
2. **Color Generation:** "Generate a color palette that matches: [personality, feel, preferences]"
3. **Typography Selection:** "Select typography that aligns with: [personality, industry]"
4. **Voice Codification:** "Define voice guidelines based on: [tone, words to avoid, examples]"

## Examples

### Example 1: Builder Brand

**Input:**
- Personality: "rugged, reliable, honest"
- Feel: "trustworthy and solid"
- Never feel: "flashy or corporate"
- Colors: "earth tones, avoid bright colors"

**Generated:**
- Colors: Deep brown primary, warm gray secondary, cream background
- Typography: Strong, readable sans-serif
- Voice: Direct, honest, no-nonsense

### Example 2: Creative Agency

**Input:**
- Personality: "creative, bold, innovative"
- Feel: "modern and inspiring"
- Never feel: "boring or traditional"
- Colors: "vibrant, unexpected"

**Generated:**
- Colors: Bold accent color, neutral base, high contrast
- Typography: Modern geometric sans
- Voice: Creative, energetic, confident

## Future Enhancements

- Logo generation from brand system
- Image style guidelines
- Animation/motion preferences
- Component style variations
