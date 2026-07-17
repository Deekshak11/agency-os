# Agency OS - Complete Architecture Documentation

## 1. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AGENCY OS - FULL STACK OVERVIEW                      │
├─────────────────────────────────────────────────────────────────────────────┤

                        ┌───────────────────────┐
                        │   OPENCODE DESKTOP    │
                        │    (Agent Runtime)    │
                        └───────────┬───────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   AGENTS.md    │         │  .opencode/     │         │    scripts/     │
│  (Constitution)│         │   (Workspace)   │         │   (Python)      │
└───────────────┘         └─────────────────┘         └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              MEMORY SYSTEM (3-LAYER)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  LAYER 1: .opencode/memory/life/     → PARA: projects/, areas/, archives/  │
│  LAYER 2: .opencode/memory/daily/    → YYYY-MM-DD.md notes                  │
│  LAYER 3: .opencode/memory/tacit/    → preferences, patterns, mistakes     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              OPENCODE WORKSPACE                              │
├────────────────┬────────────────┬─────────────────┬────────────────────────┤
│    CONFIG      │     RULES      │     AGENTS      │        SKILLS         │
├────────────────┼────────────────┼─────────────────┼────────────────────────┤
│ config.jsonc   │ coding-rules   │ researcher.md   │ ralph-loop/SKILL.md   │
│ (MiniMax 2.5)  │ memory-setup   │ code-writer.md  │ glassbox-monitor/     │
│                │                │ memory-manager  │ heartbeat/            │
│                │                │                 │ nightly-consolidation/│
└────────────────┴────────────────┴─────────────────┴────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              PYTHON SCRIPTS                                 │
├──────────────────────────────┬─────────────────────────────────────────────┤
│      PRODUCTION SCRIPTS      │              UTILITY SCRIPTS                │
├──────────────────────────────┼─────────────────────────────────────────────┤
│ modal_verified_runner_turbo  │ glassbox_core.py       (Telemetry Core)    │
│   → Asset Generation (V7)    │ glass_box_monitor.py   (Dashboard)         │
│                              │ ralph_loop_skill.py    (Loop Manager)       │
│ verified_asset_generator.py  │ export_instantly.py    (Blocked: Keys)      │
│   → V7 Core Logic            │ refresh_tokens_cloud.py (Token Mgmt)       │
│                              │                                               │
│      LIBRARY MODULES         │                                               │
│ golden_doc.py, golden_sheet  │                                               │
│ google_services.py           │                                               │
└──────────────────────────────┴─────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                 DATA LAYER                                  │
├───────────────────────────────┬───────────────────────────────────────────┤
│      LOCAL STORAGE           │           MODAL VOLUMES                     │
├───────────────────────────────┼───────────────────────────────────────────┤
│ data/                        │ agency-os-tokens                            │
│   production_1k_leads.json   │   → OAuth tokens (20+)                      │
│   production_batch2_leads.json│                                           │
│   verified_assets_turbo_v2   │ agency-os-logs                              │
│                               │   → JSONL telemetry                         │
│ templates/                   │                                             │
│   golden_sheet.csv           │                                             │
│   golden_profit_gap.md      │                                             │
│   verified_golden_leads.json│                                             │
│                               │                                             │
│ tokens/                      │                                             │
│   token_1.json ... token_21 │                                             │
└───────────────────────────────┴───────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            EXTERNAL INTEGRATIONS                            │
├───────────────────────────────┬───────────────────────────────────────────┤
│       ACTIVE / READY          │              PLANNED                       │
├───────────────────────────────┼───────────────────────────────────────────┤
│ Google APIs                   │ n8n Sales Suite                             │
│   → Drive API                │   → Self-hosted automation                   │
│   → Sheets API               │                                             │
│   → Docs API                 │ Baserow CRM                                 │
│   → OAuth 2.0 tokens         │   → Contacts table                          │
│                              │   → Deals table                              │
│ Modal Cloud                  │   → Competitors table                        │
│   → verified-fcfo-turbo-runner│                                            │
│   → Glass Box telemetry      │ Discord Lead Router                         │
│                              │   → Speed layer for hot leads                │
│ Perplexity AI                │                                             │
│   → Research data/            │ WhatsApp Concierge                          │
│                              │   → Multi-channel auto-responder             │
│                              │                                             │
│                              │ Firecrawl + OpenAI                          │
│                              │   → Deep Dive Dossier workflow              │
│                              │                                             │
│                              │ Mailgun                                     │
│                              │   → Email sending infrastructure             │
│                              │                                             │
│                              │ Twilio/SMS                                  │
│                              │   → SMS channel                             │
│                              │                                             │
│                              │ HubSpot (planned)                           │
│                              │   → Alternative CRM option                  │
└───────────────────────────────┴───────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            GLASS BOX TELEMETRY                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐               │
│  │   Script    │ ──── │  glassbox   │ ──── │   Modal     │               │
│  │  (Runner)   │ call │  _core.py    │ write│   Volume    │               │
│  └─────────────┘      └─────────────┘      └──────┬──────┘               │
│                                                     │                       │
│                                                     ▼                       │
│                                             ┌─────────────┐               │
│                                             │   logs/     │               │
│                                             │  glassbox/  │               │
│                                             │  *.jsonl    │               │
│                                             └──────┬──────┘               │
│                                                    │                       │
│                                                    ▼                       │
│                                             ┌─────────────┐               │
│                                             │  Dashboard  │               │
│                                             │  Viewer     │               │
│                                             │  (monitor)  │               │
│                                             └─────────────┘               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA FLOW DIAGRAM                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐ │
│   │  Lead    │───▶│   Modal      │───▶│   Asset     │───▶│   Google     │ │
│   │  JSON    │    │   Runner     │    │  Generator  │    │   Sheets     │ │
│   └──────────┘    └──────┬───────┘    └──────┬──────┘    └──────┬───────┘ │
│                          │                    │                   │        │
│                          │              ┌─────▼─────┐             │        │
│                          │              │ Glassbox  │             │        │
│                          │              │ Telemetry │             │        │
│                          │              └─────┬─────┘             │        │
│                          │                    │                   │        │
│                          ▼                    ▼                   ▼        │
│                    ┌────────────┐      ┌────────────┐      ┌────────────┐ │
│                    │   Modal    │      │   JSONL    │      │   GDoc     │ │
│                    │   Volume   │      │   Logs     │      │  Cloning   │ │
│                    │  (Tokens)  │      │            │      │            │ │
│                    └────────────┘      └────────────┘      └────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Inventory

### 2.1 Core Files (Root Level)

| File | Purpose | Status |
|------|---------|--------|
| `AGENTS.md` | Agent Constitution (v3.0) | ✅ Active |
| `STATUS.md` | Dashboard / Current Phase | ✅ Active |
| `MEMORY.md` | Long-term brain / Decisions | ✅ Active |
| `PRD.md` | Task specifications | ✅ Active |
| `progress.txt` | Execution log | ✅ Active |

### 2.2 Production Scripts

| Script | Purpose | Status | Key Function |
|--------|---------|--------|--------------|
| `modal_verified_runner_turbo.py` | Main asset generator | ✅ V6 VERIFIED | `process_verified_lead_turbo_v2()` |
| `verified_asset_generator.py` | V7 Core Logic | ✅ Active | `generate_verified_asset()` |
| `refresh_tokens_cloud.py` | Token refresh & sync | ✅ Active | OAuth token rotation |
| `glassbox_core.py` | Telemetry logging | ✅ Active | `log_event()` |
| `glass_box_monitor.py` | Log dashboard | ✅ Active | JSONL viewer |

### 2.3 Templates

| Template | Purpose | Status |
|----------|---------|--------|
| `golden_sheet.csv` | V6 Sheet Standard | ✅ Active |
| `golden_profit_gap.md` | Profit Gap Analysis | ✅ Active |
| `verified_golden_leads.json` | 5 Lead Examples | ✅ Active |
| `human_gdoc_template_v2.md` | GDoc Format | ✅ Active |
| `lead_magnet_gold.txt` | Lead Magnet Copy | ✅ Active |

### 2.4 OpenCode Workspace Components

| Component | Path | Status |
|-----------|------|--------|
| Config | `.opencode/config.jsonc` | ✅ MiniMax 2.5 Zen |
| Coding Rules | `.opencode/rules/coding-rules.md` | ✅ Active |
| Memory Setup | `.opencode/rules/memory-setup.md` | ✅ Active |
| Life Directory | `.opencode/memory/life/` | ✅ PARA structure |
| Daily Notes | `.opencode/memory/daily/` | ✅ YYYY-MM-DD format |
| Tacit Knowledge | `.opencode/memory/tacit/` | ✅ 4 files |
| Researcher Agent | `.opencode/agents/researcher.md` | ✅ Configured |
| Code-Writer Agent | `.opencode/agents/code-writer.md` | ✅ Configured |
| Memory-Manager Agent | `.opencode/agents/memory-manager.md` | ✅ Configured |

### 2.5 Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| `ralph-loop` | Iterative autonomous execution | ✅ Implemented |
| `glassbox-monitor` | Telemetry monitoring | ✅ Implemented |
| `heartbeat` | Long-running task monitor | ⚠️ Partial |
| `nightly-consolidation` | Memory updates | ⚠️ Partial |

---

## 3. Integration Matrix

```
                    │ Google │ Modal │ n8n │ Baserow │ Discord │ WhatsApp │ Mailgun
────────────────────┼────────┼───────┼─────┼─────────┼─────────┼──────────┼────────
Asset Generation    │   ✅   │  ✅   │  ❌  │    ❌   │    ❌   │    ❌    │    ❌
Token Management    │   ✅   │  ✅   │  ❌  │    ❌   │    ❌   │    ❌    │    ❌
Telemetry           │   ❌   │  ✅   │  ❌  │    ❌   │    ❌   │    ❌    │    ❌
CRM (Planned)       │   ❌   │  ❌   │  ❌  │    🔶   │    🔶   │    🔶    │    ❌
Outreach (Planned)  │   ❌   │  ❌   │  🔶  │    ❌   │    ❌   │    ❌    │    🔶
```

**Legend**: ✅ = Active | 🔶 = Planned | ❌ = Not Started

---

## 4. Data Assets

### 4.1 Lead Data

| File | Records | Status |
|------|---------|--------|
| `production_1k_leads.json` | ~1,000 | ✅ Verified |
| `production_batch2_leads.json` | ~1,000 | ✅ Verified |
| `production_recovery_leads.json` | ~100 | ✅ Verified |
| `verified_assets_production_batch2.csv` | Output | ✅ Generated |
| `verified_assets_turbo_v2.csv` | Output | ✅ Generated |

### 4.2 Template Data

| File | Contents |
|------|----------|
| `verified_golden_leads.json` | 5 sample leads (Stainless, Dialogue AI, COGNNA, Paramify, Cavela) |
| `golden_sheet.csv` | Sheet format standard |
| `golden_profit_gap.md` | V2 GDoc format |

---

## 5. Execution Commands

### 5.1 Core Operations

```bash
# Asset Generation (Production)
modal run scripts/modal_verified_runner_turbo.py

# Dry Run (5 leads)
modal run scripts/modal_verified_runner_turbo.py --dry-run

# Token Refresh
modal run scripts/refresh_tokens_cloud.py

# Glass Box Monitor
python scripts/glass_box_monitor.py

# Ralph Loop (Autonomous)
python scripts/ralph_loop_skill.py

# Style Check
python scripts/rebuild_golden_sheet_bulletproof.py
```

### 5.2 Git Operations

```bash
# Session End Protocol
python scripts/sync_context_to_doc.py  # Sync context
git add . && git commit -m "message"   # Commit
git push                               # Push
```

---

## 6. Executive Summary

### 6.1 What's Working Well

| Category | Assessment |
|----------|------------|
| **Asset Generation Pipeline** | ✅ Fully operational with V7 logic, GDoc cloning, Sheet personalization |
| **Glass Box Observability** | ✅ Comprehensive JSONL telemetry with dashboard viewer |
| **Token Management** | ✅ 20+ OAuth tokens with random rotation strategy |
| **OpenCode Workspace** | ✅ Complete with 3-layer memory, custom agents, 4 skills |
| **Data Assets** | ✅ ~2k verified leads, golden templates, production outputs |
| **Documentation** | ✅ SOPs, setup guides, changelog, incident reports |

### 6.2 Incomplete / Missing

| Component | Priority | Gap |
|-----------|----------|-----|
| **n8n Sales Suite** | HIGH | No instance deployed, no workflows built |
| **Baserow CRM** | HIGH | No tables, no API token configured |
| **Multi-channel Outreach** | MEDIUM | No WhatsApp, SMS, or email sending |
| **export_instantly.py** | MEDIUM | Blocked on Instantly API keys |
| **Heartbeat Monitoring** | LOW | Skill exists but not actively used |
| **Nightly Consolidation** | LOW | Skill exists but not scheduled |

### 6.3 Risks & Bottlenecks

1. **Token Exhaustion**: 20 tokens can burn out quickly under high concurrency (30 parallel)
2. **Rate Limit Cascades**: 429 errors from Google APIs cause retries and delays
3. **Stale Lead Data**: Production data from Jan 2025 - may need refresh
4. **No Automation Backbone**: n8n infrastructure missing prevents Phase 3 (concierge model)
5. **Model Dependency**: Free MiniMax model; production quality may require Anthropic

### 6.4 Recommended Next Steps (Priority Order)

1. **Deploy Baserow** → Create Contacts/Deals tables → Generate API token
2. **Spin up n8n** → Deploy via docker-compose → Connect Baserow credential
3. **Build Workflow #2** → WhatsApp Concierge → Multi-channel auto-responder
4. **Test Full Pipeline** → `modal run --dry-run` → Verify end-to-end
5. **Refresh Token Volume** → Run `refresh_tokens_cloud.py` → Ensure tokens are live

---

## 7. Architecture Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-01-20 | Unified Token Volumes | Centralize auth; mount to all runners |
| 2026-01-26 | Glass Box Architecture | JSONL telemetry for observability |
| 2026-01-26 | Ralph Loop Protocol | Iterative autonomous execution |
| 2026-01-27 | Extension vs Skill Pivot | Python scripts over VS Code extensions |
| 2026-04-06 | OpenCode Agentic Workspace | Nick Saraev + Nat Eliason methods |

---

*Generated: April 12, 2026*
*Maintained by: Antigravity AI*
