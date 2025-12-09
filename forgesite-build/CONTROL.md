# ForgeSite Build - Control Document for Otto

## Factory System Overview
ForgeSite Build is a website factory for builders, trades & shops. Otto and Cursor work together to assemble sites from modular components based on structured intake data.

## Factory Philosophy
- **No bespoke work**: All sites are built from standardized factory modules
- **Standardized modules**: Proven, tested components optimized for trades
- **Config-driven**: Sites are assembled from intake data, not custom-designed
- **Repeatable production**: The factory model enables scalable, predictable output

## Otto's Role
Otto should:
- Watch `/intake/examples` and `/leads/*` for new intake files
- Validate intake data using BusinessIntakeSchema
- Generate site configs from intake
- Build preview sites in `/app/(examples)/{slug}/`
- Generate proposals automatically
- Open PRs for review before production deploy

## Safety Boundaries
Otto MUST NOT:
- Deploy to production without approval
- Change DNS settings
- Overwrite existing client configs without backup
- Make design changes outside module system
- Bypass validation schemas

## Logging
Always log: `[OTTO ACTION] <description>`
Example: `[OTTO ACTION] Generated preview site for lead-12345`

## Workflow

### When New Intake is Received:
1. Validate using `BusinessIntakeSchema` from `/factory/schemas/intake.ts`
2. Generate site config using intake data
3. Create preview site in `/app/(examples)/{slug}/page.tsx`
4. Generate proposal using `/factory/proposal/generateProposal.ts`
5. Save proposal to `/leads/{leadId}/proposal.md`
6. Open PR for review
7. Log: `[OTTO ACTION] Generated preview site for {leadId}`

### When Intake is Updated:
1. Validate changes
2. Regenerate site config
3. Update preview site
4. Update proposal
5. Log: `[OTTO ACTION] Updated preview site for {leadId}`

## File Structure
- Intake files: `/leads/{leadId}/intake.json`
- Proposals: `/leads/{leadId}/proposal.md`
- Preview sites: `/app/(examples)/{slug}/page.tsx`
- Example intakes: `/intake/examples/*.json`

## Module System
All site pages are built using modules from `/factory/modules/`. 
Do not create custom components outside this system.

## Validation
Always validate intake data before processing:
```typescript
import { BusinessIntakeSchema } from '@/factory/schemas/intake';
const validated = BusinessIntakeSchema.parse(intakeData);
```
