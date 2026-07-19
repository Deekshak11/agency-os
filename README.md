# Agency OS (Antigravity)

**Autonomous outbound factory** for quality-first lead magnets and campaigns — batch personalization on **Modal** + **Google Workspace**, operated under agent rules (constitution, memory, status).

[![Portfolio](https://img.shields.io/badge/Portfolio-deekshak.site-0ea5e9?style=for-the-badge)](https://deekshak.site)
[![Author](https://img.shields.io/badge/Author-Deekshak%20SS-1e293b?style=for-the-badge)](https://github.com/Deekshak11)

> Public **architecture + runners + SOPs** snapshot. No client lead lists, tokens, or full private runtime.

---

## Problem

Spray-and-pray outbound destroys boutique trust. Fractional / advisory offers need **hyper-personalized** magnets at volume without a $25k/mo content army.

## Solution pattern

```text
Lead source (Apollo-class)
        │
        ▼
┌───────────────────────────────┐
│  Modal production runners      │
│  · golden template clone       │
│  · lead-specific personalize   │
│  · hard-fail on low quality    │
│  · OAuth token pool on volume  │
└───────────────┬───────────────┘
                │
                ▼
 Google Sheets + Docs (asset plane)
                │
                ▼
 Campaign / ESP handoff
```

### Verified Clone Pattern

1. Maintain **production-perfect** golden Sheet / GDoc templates  
2. Clone at scale via Workspace APIs  
3. Personalize per lead (research + copy systems)  
4. **Hard-fail** instead of silent low-quality fallbacks  
5. Auth tokens refresh on a **Modal volume** shared by runners (never baked into images)

### Agent operating system

Antigravity / OpenCode-style loop:

```text
Always read:  AGENTS → STATUS → MEMORY  before work
Write back:   STATUS / MEMORY after meaningful runs
```

Docs in `docs/` include SOPs, architecture, strategies, and system notes.

---

## Architecture highlights

| Layer | Tech / practice |
|-------|-----------------|
| Compute | Modal batch runners |
| Assets | Google Workspace APIs |
| Auth | Multi-OAuth token pool on Modal volume |
| Quality | V7-style hard-fail generators |
| Ops | AGENTS / MEMORY / STATUS files |
| Telemetry | Glass-box run logs (see SOPs) |

```text
┌────────────┐   ┌─────────────────┐   ┌──────────────────┐
│ Lead ingest│ → │ Modal factory   │ → │ Workspace assets │
└────────────┘   │ verified runners│   │ Sheets / Docs    │
                 └────────┬────────┘   └────────┬─────────┘
                          │                     │
                          ▼                     ▼
                 Agent context files     Campaign handoff
                 (AGENTS/STATUS/MEMORY)
```

---

## Repo layout

```text
docs/           Architecture, SOPs, strategies, setup, research notes
scripts/        Production and utility runners (sanitized)
README.md       This file
```

## Security

- No live OAuth tokens, service account keys, or client CSVs in this repo  
- Private full backup remains offline / private GitHub  
- Treat scripts as **patterns** — wire your own credentials  

## Related

| Repo | Role |
|------|------|
| [business-os](https://github.com/Deekshak11/business-os) | Live multi-agent product |
| [automation-systems](https://github.com/Deekshak11/automation-systems) | n8n GTM graphs |
| [deekshak-portfolio](https://github.com/Deekshak11/deekshak-portfolio) | Hire site |

## License

MIT for original code; third-party APIs subject to their terms.
