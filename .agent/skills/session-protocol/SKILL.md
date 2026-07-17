---
name: Session Protocol
description: Standard operating procedures for starting and ending coding sessions
---

# Session Protocol Skill

## Session Start Procedure
1. Read `AGENTS.md` (immutable constitution)
2. Read `STATUS.md` (current phase and objectives)
3. Read `MEMORY.md` (strategic decisions and learnings)
4. Check `golden_assets.json` for available templates
5. Verify OAuth tokens are valid (`token.json`)
6. Summarize current state to user

## Session End Procedure
1. **Update STATUS.md**: Current phase, completed tasks, next steps
2. **Update MEMORY.md**: New decisions, learnings, failures
3. **Self-Audit Checklist**:
   - [ ] Did we achieve the session objective?
   - [ ] Any API errors or failures to log?
   - [ ] Any files created that should be archived?
   - [ ] MEMORY.md still under 100 lines?
4. Archive unused scripts/logs to `_archive/`
5. Git commit and push all changes

## Context File Limits
| File | Purpose | Max Lines |
|------|---------|-----------|
| AGENTS.md | Immutable rules | No limit |
| STATUS.md | Current session | ~50 lines |
| MEMORY.md | Learnings/decisions | 100 lines |

## Self-Audit Questions
After each session, answer:
1. **What worked?** → Add to MEMORY.md as pattern to repeat
2. **What failed?** → Add to MEMORY.md as anti-pattern
3. **What's next?** → Update STATUS.md next steps

## Emergency Commands
- **Auth Repair**: `python scripts/refresh_google_oauth.py`
- **Style Check**: `python scripts/rebuild_golden_sheet_bulletproof.py`
- **Asset Fix**: `python scripts/v6_asset_rectifier.py --force`
