# Project Memory

> **The Single Source of Truth for Strategy, Decisions, and Learnings.**

---

## 🌟 North Star
> **Goal: Build a $10k/mo outbound agency for Fractional CFOs**
> **Offer**: 30-Day Free Trial -> $250/call (Performance).
> **Strategy**: "Profit Gap" Hyper-personalization (Quality > Quantity).

## Active Architecture
- **Glass Box Strategy**: Every script emits JSONL telemetry to `agency-os-logs` Modal Volume.
- **n8n Sales Suite (Next)**: Shifting from mass lead generation to a high-touch, low-volume "Concierge" ecosystem.
- **State Reification**: Monitor agents via `glass_box_monitor.py`.
- **Core Orchestrator**: `modal_verified_runner_turbo.py` (Asset Generation).

---

## 1. Tactical Specifications (The Playbook)

### Workspace Hygiene (CRITICAL)
1. **Rule**: Utility scripts must be archived at session end.
2. **Current Goal**: Focus on the 18 high-impact workflows defined in `n8n Sales Suite Design.md`.

---

## 2. Strategic Decisions

### [2026-01-26] Pivot: n8n Sales Suite over Mass Lead Gen
**Context**: Mass lead generation is hitting diminishing returns/complexity. The "Boutique Paradox" requires high-touch concierge enrichment.
**Decision**: 
1. **Pivoted**: Stopped active lead generation focus.
2. **Phase 3 Objective**: Build the "n8n Sales Suite" ecosystem (Baserow, Firecrawl, Discord).
3. **Observability**: The Glass Box will serve as the "Telemetry Layer" for these n8n workflows.

### [2026-01-26] Glass Box Architecture & Observability
**Decision**: Implemented `glassbox_core` to log events locally/cloud. Created high-contrast `agency_os_map.html`.

### [2026-01-26] Architecture Shift: Ralph Loop Protocol
**Decision**: Adopted "Ralph Loop" (Iterative Autonomous Execution) as the standard operating procedure.
**Change**:
1.  **Context**: `PRD.md` replaces ad-hoc plans. `progress.txt` replaces internal memory.
2.  **Workflow**: Shift from "Ask -> Do" to "Spec -> Loop".

### [2026-01-20] Unified Autonomous Token Management
**Decision**: Centralize all tokens in a Modal Volume. mount that volume to all Runners. Zero local sync required.

### [2026-01-27] The "Extension vs Skill" Pivot
**Context**: We attempted to use VS Code extensions (`ralph-loop`, `ralphy.sh`) for autonomous loops on Windows.
**Failure**: Extensions failed due to pathing issues (PowerShell), protocol mismatches (HTTP vs HTTPS), and reliance on external CLIs not present in the environment.
**Decision**: Abandoned extensions in favor of **Native Antigravity Skills** (Python Scripts).
**Pattern**:
- **Why**: "Glass Box" visibility. We can see and edit `scripts/ralph_loop_skill.py`.
- **How**: The script acts as the "Manager", generating prompts for the Agent.
- **Protocol**: Rigidly enforced "Plan -> Code -> Verify -> Commit -> Loop" (Wiggum Technique).

---

## 🏗 Architectural Patterns

### The "Autonomous Volume" Pattern
Centralize authentication tokens and logs in separate Modal Volumes. Never bake tokens into images; mount them.

### n8n-First Automation
Targeting $0 enterprise "SaaS tax". Use self-hosted n8n + Baserow + Discord instead of HubSpot/Salesforce.
### [2026-04-16] OTEL Tracing + LangSmith Observability
**Context**: Need LangChain-style "flight recorder" for AI agent tracing - visibility into LLM calls, tool executions, agent decisions, bottlenecks.
**Decision**:
1. Implemented `scripts/otel_tracing.py`: OTEL-compatible tracing with LangSmith backend
2. Created `scripts/modal_otel_runner.py`: Modal runner with full instrumentation
3. Created `.opencode/otel_env.template`: Environment configuration for LangSmith OTEL
4. Updated glassbox-monitor skill to document both layers (JSONL + OTEL)

**Key Files**:
- `scripts/otel_tracing.py` - Core tracing module (trace_span, trace_llm_call, trace_tool_execution, trace_agent_loop, TracedRunner)
- `scripts/modal_otel_runner.py` - Modal runner template with OTEL
- `.opencode/otel_env.template` - LangSmith API key + OTEL config

**Setup**: Copy otel_env.template to .env, add LANGSMITH_API_KEY, install otel packages.

### [2026-04-06] OpenCode Agentic Workspace Setup
**Context**: Researched Nick Saraev's Claude Code courses (4hr + 3hr Advanced) and Nat Eliason's OpenClaw methods to implement agentic workspace on OpenCode desktop app.
**Decision**: 
1. Created `.opencode/config.jsonc` with MiniMax 2.5 Zen model (free)
2. Enhanced `AGENTS.md` to v3.0 (CLAUDE.md spec) with Mode System
3. Implemented 3-layer memory system (Life Directory, Daily Notes, Tacit Knowledge)
4. Created custom sub-agents (researcher, code-writer, memory-manager)
5. Created Skills for workflows (ralph-loop, glassbox-monitor, heartbeat, nightly-consolidation)

**Key Files Created**:
- `.opencode/config.jsonc` - Model config
- `.opencode/rules/coding-rules.md` - Coding standards
- `.opencode/rules/memory-setup.md` - Memory system guide
- `.opencode/memory/life/` - PARA directory
- `.opencode/memory/daily/` - Daily notes
- `.opencode/memory/tacit/` - Preferences, patterns, mistakes, security
- `.opencode/agents/researcher.md` - Research sub-agent
- `.opencode/agents/code-writer.md` - Code generation sub-agent
- `.opencode/agents/memory-manager.md` - Memory management sub-agent
- `.opencode/skills/*/SKILL.md` - Workflow skills

**Key Techniques Implemented**:
- Plan Mode (Tab key toggle) for analysis
- Edit Mode for quick execution
- 3-Layer Memory System from Nat Eliason
- Ralph Loop for autonomous execution
- Heartbeat for long-running task monitoring
- Nightly Consolidation for memory updates

---

*Maintained by: Antigravity AI | Last Updated: Apr 6, 2026*
