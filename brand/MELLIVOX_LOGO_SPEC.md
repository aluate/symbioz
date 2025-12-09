# Mellivox Logo & Design Specifications

## Logo Philosophy

The Mellivox bee sigil is a **sacred mark**, not a corporate logo. It should feel like:
- A forbidden seal discovered on temple ruins
- An archivist's mark
- An ancient biotech order's insignia

## Design Requirements

### Bee Sigil (Mark Only)

- **Structure:**
  - Single hexagon "gate" as container
  - Bee built from 3–5 minimalist strokes
  - Wings as angular arcs, almost runic
  - Thorax formed by a hex cell
  - Symmetrical, ritualistic shape

- **Style:**
  - Geometric > realism
  - Minimalist lines
  - Zero cartoon proportions
  - No beveled outlines
  - No rounded wings
  - No fluffy stripe spacing
  - No googly eyes or humanized features

- **Colors:**
  - Primary: Vox Gold (`#C69A3E`) on Hive Black (`#0B0B0F`)
  - Alternative: Black on Pollen Ivory (`#EDE8D1`) for light backgrounds

### Logo Lockup (Mark + Wordmark)

- **Wordmark:** "MELLIVOX" in serif with ancient angles
- **Spacing:** Mark and wordmark separated by appropriate gap
- **Alignment:** Horizontal lockup preferred

## DAC Notes (Logo-Specific)

The bee sigil should **never** be rendered in a "cute" or cartoon style. It must always feel:
- Solemn
- Forbidden
- Ancient
- Ritualistic

**Avoid:**
- Roundness or cartoon proportions
- Cutesy styling
- Activism branding
- Hipster coffee brand vibes
- Children's eco-toy aesthetics
- Etsy Queen Bee merch style

**The moment it humanizes or smiles, Mellivox dies.**

## File Structure

Recommended repo structure:

```
/public
  /mellivox
    mellivox-logo-dark.png      # Full logo on dark background
    mellivox-mark.svg           # Bee in hex only
    mellivox-lockup.svg         # Bee + wordmark
    mellivox-mark-light.svg     # Optional, for light backgrounds
```

## Usage Examples

### In Next.js Component

```tsx
import Image from "next/image";

export function MellivoxLogo() {
  return (
    <div className="flex items-center gap-3">
      <Image
        src="/mellivox/mellivox-lockup.svg"
        alt="Mellivox"
        width={260}
        height={130}
        priority
      />
    </div>
  );
}
```

### Mark-Only (Nav Icon)

```tsx
<Image
  src="/mellivox/mellivox-mark.svg"
  alt="Mellivox mark"
  width={40}
  height={40}
/>
```

## Favicon

Export a 512×512 PNG version of the mark (bee in hex) on Hive Black background.

Use a favicon generator to create:
- `favicon.ico`
- `apple-touch-icon.png`
- etc.

Drop them in `/public` and ensure `app/layout.tsx` or `_document.tsx` has appropriate `<link rel="icon" ...>` tags.

---

See `MELLIVOX_BRAND_BIBLE.md` for full brand documentation.

