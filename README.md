# Agency OS (Antigravity)

**Autonomous outbound production system** — quality-first lead magnets and personalized campaigns for Fractional CFOs / B2B niches, orchestrated by an agent runtime (“Antigravity”) on **Modal + Google Workspace**.

| | |
|---|---|
| **Author** | [Deekshak SS](https://deekshak.site) |
| **Portfolio** | [deekshak.site](https://deekshak.site) |
| **Era** | Late 2025 – early 2026 |
| **Related private backup** | `Deekshak11/Agency_OS` |

---

## North star

> Build a **performance outbound engine** for Fractional CFOs (and adjacent B2B niches):  
> **$0 setup · 30-day free trial · $250 / qualified call** after trial.  
> Strategy: **“Profit Gap”** — quality assets over spray-and-pray volume.

## What it is

Not a chatbot demo. A **factory**:

```
Verified leads (Apollo-class)
        ↓
Modal runner (token pool + concurrency)
        ↓
Clone “Golden” Sheets + GDocs (style-preserving personalization)
        ↓
CSV / campaign handoff (Instantly-class when keys available)
        ↓
Telemetry (Glass Box logs on Modal volumes)
```

**Antigravity** is the agent persona + operating system for this repo: constitution (`AGENTS.md`), live dashboard (`STATUS.md`), long-term brain (`MEMORY.md`), deterministic Python over vibe coding.

## Architecture (summary)

| Layer | Role |
|-------|------|
| **Agent constitution** | `docs/AGENTS.md` — rules, session end, anti-patterns |
| **Memory** | `docs/MEMORY.md` — north star, decision log, golden specs |
| **Status** | `docs/STATUS.md` — phase, objectives, blockers |
| **Python production** | `scripts/modal_verified_runner_turbo.py`, `verified_asset_generator.py` |
| **Auth** | Modal volume `agency-os-tokens` + cloud refresh (never bake keys into images) |
| **Google Workspace** | Drive / Sheets / Docs API for clone + personalize |
| **Skills** | `.agent/skills/` — lead-generation, asset-cloning, session-protocol |

Full diagram: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

## Key production patterns (learned the hard way)

1. **Verified Clone Pattern** — clone a production asset that already works; don’t re-generate from contaminated masters.  
2. **Autonomous Volume Pattern** — OAuth tokens live on a Modal volume mounted by refresher + runners.  
3. **Hard-fail over silent fallback** — low-quality turbo batch rejected; generator refactored to fail loudly.  
4. **Golden Sheet / GDoc specs (V6–V7)** — pixel heights, bolding runs, smart-chip naming rules.  
5. **Batch economics** — 1k-lead production batches with 20+ OAuth tokens and concurrency.

## What’s in this public repo

| Path | Contents |
|------|----------|
| `docs/` | Architecture, PRD, sales-suite design, SOPs, research notes |
| `scripts/` | Production runners + utilities (no credentials) |
| `.agent/skills/` | Agent skills for lead gen & cloning |
| `docs/BIZ_PROJECT_CONTEXT.txt` | Synced Antigravity context (Biz Project) |

**Not published:** OAuth tokens, credential files, production lead CSVs, Instantly keys, private client data.

## Stack

Python · Modal · Google Workspace APIs · Perplexity research · campaign ESP (Instantly-class) · OpenCode / Antigravity agent workspace

## Quick start (local, no secrets)

```powershell
# Review docs first
# docs/ARCHITECTURE.md · docs/MEMORY.md · docs/AGENTS.md

# Scripts expect Google OAuth + Modal secrets configured locally (never commit)
cd scripts
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# pip install -r requirements if present
# modal run modal_verified_runner_turbo.py  # after secrets
```

## Relation to other projects

| Project | Link |
|---------|------|
| Show-Rate Guardian | [show-rate-guardian](https://github.com/Deekshak11/show-rate-guardian) |
| Signal OS / Mission Control | [signal-os](https://github.com/Deekshak11/signal-os) |
| Business OS product | [business-os](https://github.com/Deekshak11/business-os) · [app.deekshak.site](https://app.deekshak.site) |

## License

MIT for original documentation and scripts in this public snapshot.  
Third-party APIs subject to their terms. Private operational data remains private.
