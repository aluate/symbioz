# Automation Tasks for Otto

## V1 Safe Tasks (Implement Now)
- ✅ Generate example configs from intake JSON
- ✅ Scaffold new client site configs
- ✅ Draft proposals from intake
- ✅ Open PRs for new client sites
- ✅ Validate intake data before processing
- ✅ Watch for new intake files in `/leads/`
- ✅ Generate preview sites from validated intake

## V2+ Tasks (Future, NOT Now)
- ⏸️ Automated DNS updates
- ⏸️ Auto-deploy on intake approval
- ⏸️ Schedule-based code changes
- ⏸️ AI bot conversation handling (full implementation)
- ⏸️ Automated email sequences
- ⏸️ Automated client onboarding workflows
- ⏸️ Automated site updates from chat bot requests

## Task Details

### Generate Preview Site
**Trigger:** New intake file in `/leads/{leadId}/intake.json`
**Actions:**
1. Read and validate intake JSON
2. Generate SiteConfig from intake
3. Create preview page at `/app/(examples)/{slug}/page.tsx`
4. Generate proposal markdown
5. Save proposal to `/leads/{leadId}/proposal.md`
6. Open PR with changes

### Validate Intake
**Trigger:** Before any processing
**Actions:**
1. Load intake JSON
2. Validate with BusinessIntakeSchema
3. Log validation errors if any
4. Stop processing if validation fails

### Generate Proposal
**Trigger:** After intake validation
**Actions:**
1. Call `generateProposal()` from `/factory/proposal/generateProposal.ts`
2. Save markdown to `/leads/{leadId}/proposal.md`
3. Log success

## Error Handling
- Always log errors with context
- Never silently fail
- Alert on validation failures
- Backup before overwriting files

## Testing
Before implementing new automation:
1. Test with example intake files
2. Verify validation works
3. Check generated output
4. Test error cases
