# Comprehensive Guide: Anthropic Agent Frameworks Architecture & Implementation

**Date Created:** January 7, 2026  
**Research Focus:** MCP, Agent Skills, Agent SDK, and Antigravity IDE Integration  
**Source:** Official Anthropic Documentation + Expert Implementation Resources

---

## Executive Summary

This document provides a complete architecture guide for implementing AI agents using Anthropic's latest frameworks:
- **Model Context Protocol (MCP)** - Standardized data integration framework
- **Agent Skills** - Reusable, filesystem-based domain expertise modules
- **Claude Agent SDK** - Complete agent harness with built-in capabilities
- **Antigravity IDE** - Google's agentic development platform (compatible with Claude Code)

The guide covers:
1. Architecture patterns and best practices
2. How to implement each framework effectively
3. Integration strategies for Antigravity IDE
4. Real-world implementation considerations
5. Context management for long-running agents

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [The Agent Loop Pattern](#the-agent-loop-pattern)
3. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
4. [Agent Skills Framework](#agent-skills-framework)
5. [Claude Agent SDK](#claude-agent-sdk)
6. [Antigravity IDE Integration](#antigravity-ide-integration)
7. [Best Practices & Design Principles](#best-practices--design-principles)
8. [Implementation Checklist](#implementation-checklist)
9. [Security & Deployment](#security--deployment)

---

## Architecture Overview

### Core Philosophy

Anthropic's agent architecture is built on three core principles:

1. **Simplicity** - Start with simple LLM calls, add complexity only when needed
2. **Transparency** - Show agent reasoning steps explicitly
3. **Composability** - Build with reusable, modular components

### When to Use Agents vs. Simpler Approaches

| Approach | Best For | Trade-offs |
|----------|----------|-----------|
| Single LLM Call | Simple transformations, classification | Low cost, low latency, limited capability |
| Prompt Chaining | Sequential tasks with clear steps | Higher cost, moderate latency |
| Routing | Different tasks requiring specialized handling | Better accuracy for specific task types |
| Workflows | Well-defined, predictable task flows | Predictability, good for regulated environments |
| **Agents** | **Open-ended, complex, adaptive tasks** | **Higher cost/latency, requires trust in model** |

### Workflow vs. Agent Distinction

**Workflows:**
- LLMs orchestrated through predefined code paths
- Fixed task flow determined by developers
- Predictable, consistent, deterministic
- Examples: Prompt chaining, routing, orchestrator-workers patterns

**Agents:**
- LLMs dynamically direct their own processes
- Model determines tool usage and execution flow
- Flexible but requires environmental feedback
- Examples: Autonomous coding agents, research agents, customer support agents

---

## The Agent Loop Pattern

### Core Framework: Gather Context → Take Action → Verify Work

All effective agents follow this repeating cycle:

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT LOOP CYCLE                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. GATHER CONTEXT                                         │
│     ├─ Agentic search (filesystem, bash, grep)           │
│     ├─ Semantic search (vector embeddings)               │
│     ├─ Subagents for parallel information gathering      │
│     └─ Compaction for long-running tasks                 │
│                                                             │
│  2. TAKE ACTION                                            │
│     ├─ Tools (primary, high-context-visibility)          │
│     ├─ Bash/Scripts (flexible, deterministic)            │
│     ├─ Code Generation (complex operations)              │
│     └─ MCP Integrations (external services)              │
│                                                             │
│  3. VERIFY WORK                                            │
│     ├─ Rule-based feedback (linting, validation)         │
│     ├─ Visual feedback (screenshots, renders)            │
│     └─ LLM as judge (fuzzy evaluation)                   │
│                                                             │
│  [↻ REPEAT until task complete]                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Phase 1: Gather Context

**Agentic Search (Preferred)**
- Uses filesystem navigation: `ls`, `grep`, `find`, `cat`
- Explicit, debuggable, transparent
- Better for variable file structures
- Recommended starting approach

```bash
# Agent navigates filesystem to gather context
ls -la project/
grep -r "function_name" src/
cat file.txt | tail -20
```

**Semantic Search (Supplementary)**
- Uses vector embeddings for similarity matching
- Faster but less transparent
- Use only if agentic search insufficient
- Harder to debug and maintain

**Subagents for Parallelization**
- Spin up multiple agents to work on different information gathering tasks
- Each subagent has isolated context window
- Return only relevant excerpts to main orchestrator
- Ideal for: searching multiple sources, parallel analysis

**Context Compaction for Long Sessions**
- Automatically summarizes old messages when context approaches limit
- Preserves agent understanding across sessions
- Critical for multi-hour/multi-day agent runs

### Phase 2: Take Action

**Tool Design Hierarchy**

| Priority | Component | Use Case | Context Cost |
|----------|-----------|----------|--------------|
| 1 | **Tools** | Primary, frequent actions | High (always visible) |
| 2 | **Bash/Scripts** | General computer access | Low (output only) |
| 3 | **Code Generation** | Complex, deterministic operations | None (code is output) |
| 4 | **MCP Integrations** | External service access | Medium (standardized) |

**Tools - Primary Actions**

Guidelines for effective tool design:
- Should represent the most frequent agent actions
- Keep tool count reasonable (5-15 for best performance)
- Comprehensive documentation with examples
- Clear parameter definitions with validation

```json
{
  "name": "searchEmails",
  "description": "Search user's email history by keywords, sender, date range. Returns email summaries with IDs.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search keywords or sender name"
      },
      "dateFrom": {
        "type": "string",
        "description": "ISO 8601 date format (YYYY-MM-DD)"
      }
    },
    "required": ["query"]
  }
}
```

**Bash/Scripts - Flexible Execution**

- Write and execute Python, JavaScript, bash scripts
- Code never loads into context (only output does)
- Use for: file operations, data processing, API calls
- More efficient than LLM-generated code for simple operations

**Code Generation - Precise Operations**

- LLM writes code for complex operations
- Use for: building tools, creating workflows
- Advantages: infinitely composable, precise output
- Example: Claude writes Python to create Excel spreadsheets with formatting

**MCP (Model Context Protocol) - External Integrations**

- Standardized way to connect external services
- No custom OAuth/API management needed
- Pre-built servers: Slack, GitHub, Google Drive, Asana
- Seamless integration with agent workflows

### Phase 3: Verify Work

**Rule-Based Feedback (Recommended)**

Most effective verification approach:
- Define clear rules for correctness
- Run linters, validators on outputs
- Provide specific error messages
- Example: TypeScript linting provides multiple layers of feedback

```bash
# Verify generated code before delivery
eslint generated_file.js
typescript --noEmit
```

**Visual Feedback**

For UI/visual tasks:
- Screenshot rendered output
- Verify layout, spacing, colors
- Check responsive design
- Test interactive elements

Tools: Playwright MCP for automation

**LLM as Judge**

- Have another LLM evaluate agent output
- Use for fuzzy evaluation (tone, style, quality)
- More expensive, useful for high-stakes tasks
- Example: Judge agent evaluates email tone against user's communication style

---

## Model Context Protocol (MCP)

### What is MCP?

**Definition:** Open standard for connecting AI assistants to data systems and tools with a standardized interface.

**Problem it solves:**
- Before MCP: N×M problem - each LLM needed custom connector for each data source
- With MCP: Single standardized protocol for all integrations

**Release:** November 2024 by Anthropic (open-sourced)  
**Status:** Rapidly adopted by OpenAI, Google DeepMind, and entire AI ecosystem

### MCP Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Architecture                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  MCP HOST (AI Application)                                 │
│  ├─ Claude Code                                            │
│  ├─ Claude Desktop                                         │
│  ├─ Claude Agent SDK                                       │
│  └─ Custom Applications                                    │
│         ↓ (creates MCP clients)                            │
│  ┌─────────────────────────────────┐                       │
│  │   MCP CLIENT (Connection Pool)   │                       │
│  ├─────────────────────────────────┤                       │
│  │ Manages connections to servers  │                       │
│  │ Handles lifecycle mgmt          │                       │
│  │ Routes requests to servers      │                       │
│  └─────────────────────────────────┘                       │
│         ↓ (JSON-RPC over transport)                        │
│  ┌─────────────────────────────────┐                       │
│  │   MCP SERVERS (Context Providers)│                       │
│  ├─────────────────────────────────┤                       │
│  │ Tools (executable functions)    │                       │
│  │ Resources (data sources)        │                       │
│  │ Prompts (interaction templates) │                       │
│  └─────────────────────────────────┘                       │
│         ↓ (Stdio or HTTP transport)                        │
│  ┌─────────────────────────────────┐                       │
│  │   BACKEND SYSTEMS               │                       │
│  ├─────────────────────────────────┤                       │
│  │ APIs, Databases, File Systems   │                       │
│  │ Business Tools, Data Warehouses │                       │
│  └─────────────────────────────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### MCP Layers

**Data Layer**
- JSON-RPC 2.0 based protocol
- Defines primitives: Tools, Resources, Prompts
- Lifecycle management (initialize, operate, shutdown)
- Notification system for real-time updates

**Transport Layer**
- **Stdio:** Local process communication (optimal for local MCP servers)
- **Streamable HTTP:** Remote server communication (supports standard HTTP auth, OAuth)

### MCP Primitives

#### 1. Tools (AI-Invokable Functions)

Functions that the LLM can call to perform actions.

**Characteristics:**
- LLM-controlled (model decides when to invoke)
- Executable (produce actual effects)
- Examples: API calls, file operations, database queries

**Tool Discovery Flow:**
```
Client: "tools/list" → Server lists all available tools
Client: "tools/call" + tool_name + parameters → Server executes
```

#### 2. Resources (Data Sources)

Read-only data that provides context to the AI.

**Characteristics:**
- Application-controlled (app decides what to expose)
- Read-only (no modification)
- Examples: file contents, API responses, database records

**Resource Access Flow:**
```
Client: "resources/list" → Server lists available resources
Client: "resources/read" + resource_uri → Server returns data
```

#### 3. Prompts (Interaction Templates)

Reusable prompt templates that structure interactions.

**Characteristics:**
- User-controlled (triggered by user actions)
- Pre-defined instructions
- Examples: Slash commands, system prompts, few-shot examples

### Building an MCP Server

**Basic Structure:**

```python
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize server
mcp = FastMCP("your-server-name")

# Define tools using decorators
@mcp.tool()
async def your_tool_name(param1: str, param2: int) -> str:
    """Tool description for Claude to understand when to use it.
    
    Args:
        param1: Description of parameter
        param2: Description of parameter
    """
    # Tool implementation
    result = await perform_action(param1, param2)
    return result

# Run the server
def main():
    mcp.run(transport="stdio")  # or "http"

if __name__ == "__main__":
    main()
```

**Key Best Practices:**

1. **Use descriptive tool names:** `search_emails` not `find`
2. **Comprehensive docstrings:** Include what tool does and when to use it
3. **Type hints:** Help Claude understand parameter requirements
4. **Error handling:** Return clear error messages
5. **Logging:** Use stderr (never stdout for stdio servers)
6. **Tool discovery:** Always support `tools/list` properly

### MCP Lifecycle: Initialization Sequence

```json
// Step 1: Client sends initialize
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": { "elicitation": {} },
    "clientInfo": { "name": "Claude Code", "version": "2.0.0" }
  }
}

// Step 2: Server responds with capabilities
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "tools": { "listChanged": true },
      "resources": {},
      "prompts": {}
    },
    "serverInfo": { "name": "weather-server", "version": "1.0.0" }
  }
}

// Step 3: Client sends initialized notification
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

### Real-Time Updates with Notifications

MCP supports dynamic capability changes:

```json
// Server notifies client that tools have changed
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}

// Client responds by refreshing tool list
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

### Ecosystem of MCP Servers

**Official/Popular MCP Servers (2025):**
- Filesystem (read/write local files)
- GitHub (repository operations)
- Google Drive (file access)
- Slack (messaging integration)
- Asana (project management)
- Sentry (error tracking)
- Testsprite (automated testing)
- [Browse full registry: modelcontextprotocol.io](https://modelcontextprotocol.io)

---

## Agent Skills Framework

### What are Agent Skills?

**Definition:** Filesystem-based, organized folders of instructions, scripts, and resources that agents can dynamically discover and load.

**Analogy:** Like an onboarding guide for a new team member - provides domain-specific expertise on-demand.

**Release:** October 2025 by Anthropic  
**Status:** Open standard, available across Claude.ai, Claude Code, Agent SDK, API

### Progressive Disclosure Design

Core principle: Load information in stages as needed, not all at once.

```
LEVEL 1: METADATA (Always Loaded)
├─ name: "pdf-processing"
├─ description: "Extract text and tables from PDFs..."
└─ Token cost: ~100 tokens per skill

LEVEL 2: INSTRUCTIONS (Loaded When Triggered)
├─ SKILL.md (main body)
├─ Quick start examples
├─ Common workflows
└─ Token cost: Under 5k tokens

LEVEL 3+: RESOURCES (Loaded As Needed)
├─ forms.md (form-filling guide)
├─ reference.md (detailed API docs)
├─ scripts/ (executable utilities)
├─ examples/ (sample templates)
└─ Token cost: Effectively unlimited (files not loaded until accessed)
```

### Skill Directory Structure

```
my-skill/
├── SKILL.md                    # Required: Main skill file with YAML frontmatter
├── forms.md                    # Optional: Form-filling instructions
├── reference.md                # Optional: Detailed API reference
├── examples/
│   ├── example1.pdf           # Optional: Sample templates/examples
│   └── example2.json
└── scripts/
    ├── extract_fields.py      # Optional: Executable utilities
    └── validate.py
```

### SKILL.md Structure

**Required Format:**

```markdown
---
name: your-skill-name
description: Brief description of what this skill does and when Claude should use it
---

# Skill Title

## Quick Start

Step-by-step guide to get started quickly.

## How It Works

Explain the workflows and best practices.

## Examples

Concrete examples of using this skill.

For advanced topics, see [FORMS.md](FORMS.md).
```

**YAML Frontmatter Requirements:**

| Field | Required | Purpose | Example |
|-------|----------|---------|---------|
| `name` | Yes | Unique skill identifier | `pdf-processing` |
| `description` | Yes | Claude uses to determine when to trigger skill | `Extract text and tables from PDFs. Use when...` |

**Key Guidelines:**

1. **Name:** Lowercase, hyphenated, descriptive
2. **Description:** Include both WHAT it does and WHEN to use it
3. **Main body:** Clear, procedural guidance (not just links)
4. **References:** Use markdown links to related files for complex topics
5. **Examples:** Concrete, copy-paste ready examples

### Context Window Impact

```
Initial Context:
├─ System prompt
├─ Skill metadata (name + description) × N
└─ User's first message
   └─ Total: ~2-3k tokens

When Skill Triggered:
├─ Previous context
├─ SKILL.md file loaded via bash
└─ Additional context: ~2-5k tokens

If Skill References Other Files:
├─ forms.md loaded (when needed)
├─ scripts/validate.py executed (output only)
└─ examples/template.pdf read (when referenced)
```

### Skill Development Best Practices

**1. Start with Evaluation**
- Identify specific gaps in your agent's capabilities
- Run representative test cases
- Observe where agent struggles or requests repetitive information
- Build skills to address these specific gaps

**2. Structure for Scale**
- When SKILL.md becomes unwieldy (>10k tokens), split into separate files
- Keep mutually exclusive content in separate files to reduce token usage
- Use code for both execution AND documentation

**3. Progressive Enhancement**
- Start with minimal SKILL.md
- Add linked files only when needed
- Let actual usage patterns guide expansion

**4. Iterate with Claude**
- Ask Claude to capture successful workflows into the skill
- Review failures and ask Claude for self-reflection
- Let Claude help identify what context is actually needed

**5. Security Auditing**
- Only install skills from trusted sources
- Thoroughly audit untrusted skills before use
- Pay attention to:
  - External network connections
  - File system access patterns
  - Code dependencies
  - Data handling practices

### Available Pre-Built Skills (2025)

Anthropic provides official skills for common tasks:

| Skill | Purpose | Availability |
|-------|---------|--------------|
| PDF | Extract text, fill forms, merge documents | Claude API, claude.ai |
| PowerPoint | Create/edit presentations, manage slides | Claude API, claude.ai |
| Excel | Create/edit spreadsheets, manage data | Claude API, claude.ai |
| Word | Create/edit documents, manage formatting | Claude API, claude.ai |

All follow same progressive disclosure pattern.

### Skills vs. MCP: Complementary Roles

**Agent Skills:**
- For procedural workflows and domain expertise
- Filesystem-based, managed by users
- Teaching agents "how to do" complex tasks
- Example: PDF form-filling workflow

**MCP (Model Context Protocol):**
- For external service integration
- API-based, standardized protocol
- Connecting to APIs, databases, external tools
- Example: Slack integration for messaging

**Best Practice:** Use Skills for workflows + MCP for external integrations

---

## Claude Agent SDK

### Overview

**What:** Complete agent harness powering Claude Code, now generalized  
**Based on:** 6+ months of Claude Code production experience  
**Contains:** Solved infrastructure for: memory management, permissions, subagents  
**Status:** Production-ready, available via API/npm

### Core Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Agent SDK Architecture                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  AGENT HARNESS                                              │
│  ├─ Tools                    [Primary actions]              │
│  ├─ Prompts                  [System instructions]          │
│  ├─ File System              [Context source]               │
│  ├─ Skills                   [Domain expertise]             │
│  ├─ Subagents               [Parallel workers]             │
│  └─ Memory                   [Session state]                │
│         ↓                                                    │
│  AGENT LOOP (Gather Context → Act → Verify)                │
│         ↓                                                    │
│  EXECUTION ENVIRONMENT                                      │
│  ├─ Bash (Linux commands)                                   │
│  ├─ Code Execution (Python, JavaScript, etc.)              │
│  ├─ File Operations                                         │
│  └─ MCP Integrations                                        │
│         ↓                                                    │
│  OUTPUT & FEEDBACK                                          │
│  ├─ Tool results                                            │
│  ├─ Error messages                                          │
│  ├─ Linting feedback                                        │
│  └─ Environment state                                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Gathering Context: Multi-Strategy Approach

**1. Agentic Search (Primary)**
```bash
# Agent navigates filesystem directly
ls -la src/
grep -r "function_name" .
find . -name "*.py" -type f
```

**Advantages:**
- Transparent and debuggable
- Explicit file navigation
- Works well with variable structures
- No semantic search overhead

**2. Semantic Search (Supplementary)**

For when agentic search is insufficient:
- Vector embeddings of content
- Fast similarity matching
- Less transparent than agentic search
- Optional, not recommended as default

**3. Subagents (Parallel Gathering)**

For large-scale information gathering:

```python
# Pseudocode: Orchestrator spawning subagents
agent.spawn_subagent(
    task="Search email history for contracts",
    constraints={"max_tokens": 5000}
)
agent.spawn_subagent(
    task="Analyze recent invoices for patterns",
    constraints={"max_tokens": 5000}
)
results = agent.wait_for_subagents()
```

**Benefits:**
- Parallelized information gathering
- Isolated context per subagent
- Subagents return only relevant excerpts
- Main orchestrator avoids context explosion

**4. Compaction (Long-Running Sessions)**

Automatic summarization as context approaches limits:

```
Session Start:
├─ Early turns: Full context retained
├─ Mid-session: Approaching limit → Compaction triggers
│  └─ Older messages summarized automatically
└─ Later turns: Continue with summarized context
```

**Key:** Compaction preserves agent understanding while managing context limits.

### Taking Action: Tool Design

**Tool Prominence Matters**

Tools are the FIRST actions Claude considers because they're always visible in context.

```
Context Window Visibility:
┌─────────────────────────────┐
│ Always visible:             │
│ ├─ System prompt            │
│ ├─ Tools definitions        │ ← Claude prioritizes these
│ └─ Current task             │
├─────────────────────────────┤
│ Only visible if referenced: │
│ ├─ Skills                   │
│ └─ Bash/Code options        │
└─────────────────────────────┘
```

**Best Practices for Tool Design:**

1. **Limit tool count:** 5-15 tools optimal
2. **Clear names:** `searchEmails` not `find`
3. **Detailed descriptions:**
   - What the tool does
   - When to use it
   - Example inputs/outputs
   - Error cases

4. **Type validation:** Use JSON schemas strictly
5. **Poka-yoke design:** Make mistakes harder to make

**Example: Email Agent Tools**

```python
# Good tool design - specific, well-documented
@agent.tool()
async def search_emails(
    query: str,
    date_from: Optional[str] = None,
    max_results: int = 20
) -> List[EmailSummary]:
    """Search email history with full-text search.
    
    Use this when:
    - User asks about past emails
    - You need to find specific conversations
    - Checking for previous communications
    
    Args:
        query: Search keywords or sender name
        date_from: ISO 8601 format (YYYY-MM-DD)
        max_results: Cap results to avoid oversized responses
    
    Returns:
        List of email summaries with IDs for further retrieval
        
    Example:
        results = search_emails("budget proposal", date_from="2025-01-01")
        for email in results:
            print(f"{email.from}: {email.subject}")
    """
    # Implementation
    pass
```

### Verifying Work

**1. Rule-Based Verification (Recommended)**

Most reliable approach:

```bash
# Example: Verify generated TypeScript code
eslint generated_component.ts      # Syntax errors
tsc --noEmit                       # Type errors
prettier --check generated_*.ts    # Style consistency
```

Return specific error messages to Claude for correction.

**2. Visual Feedback**

For UI/visual tasks:

```python
# Example: Screenshot rendering for verification
from playwright.async_api import async_playwright

async def verify_ui():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        await page.goto("http://localhost:3000")
        screenshot = await page.screenshot()
        return screenshot  # Return to Claude for visual verification
```

Claude can then verify:
- Layout correctness
- Spacing and alignment
- Color/styling accuracy
- Responsive behavior

**3. LLM as Judge (Expensive)**

For fuzzy evaluation:

```python
# Use another Claude instance to evaluate output
judge_response = await judge_agent.evaluate(
    output=agent_output,
    criteria="Does this email match the user's communication style?"
)
```

Trade-off: Better quality but 2x cost.

### Memory & Context Management for Long-Running Agents

**The Challenge:**

Agents need to work across multiple context windows (sessions). Without proper memory:
- Agent loses context of previous work
- Repeats completed tasks
- Can't understand multi-day projects

**Solution: Two-Part Approach**

**Part 1: Initializer Agent (First Session)**

```python
# Initial session setup
initializer_prompt = """
You are setting up a new project. Create:
1. init.sh - Initialization script
2. claude-progress.txt - Progress log
3. git commit - Initial state snapshot

These will help future sessions understand what you've done.
"""
```

Creates foundation:
- `init.sh` - Reproducible setup
- `claude-progress.txt` - What was accomplished
- Git history - State snapshots

**Part 2: Coding Agent (Subsequent Sessions)**

```python
# Later session
coding_prompt = """
Review claude-progress.txt to understand previous work.
Make incremental progress on the next task.
Update claude-progress.txt with what you accomplished.
Leave clear artifacts for the next session.
"""
```

Each session:
- Reads progress file
- Makes incremental improvements
- Updates progress file
- Commits to git

**Progress File Example:**

```
# Project Progress Log

## Session 1 (Jan 7, 10:00 AM)
- Analyzed requirements in README.md
- Created initial project structure
- Implemented core database models
- Status: Models complete, API endpoints pending

## Session 2 (Jan 7, 2:00 PM)
- Reviewed models from Session 1
- Implemented REST API with 8 endpoints
- Added authentication middleware
- Status: API complete, testing pending

## Next Steps
- Write test suite
- Add error handling
- Deploy to staging
```

**Key Insight:** With proper initialization and progress tracking, agents can handle projects spanning days/weeks.

### Subagent Architecture

**When to Use Subagents:**

1. **Parallel work** - Multiple independent tasks
2. **Isolation** - Isolate context to prevent token explosion
3. **Specialization** - Use different prompts for different roles

**Example: Research Orchestrator**

```python
research_agent.spawn_subagent(
    name="source_search",
    task="Search academic databases for AI safety papers",
    constraints={"max_tokens": 4000}
)

research_agent.spawn_subagent(
    name="policy_research",
    task="Analyze government AI policy documents",
    constraints={"max_tokens": 4000}
)

research_agent.spawn_subagent(
    name="industry_analysis",
    task="Research industry AI implementations",
    constraints={"max_tokens": 4000}
)

# Main agent integrates subagent findings
results = research_agent.wait_for_subagents()
synthesis = research_agent.synthesize(results)
```

**Benefits:**
- Parallel processing (faster)
- Isolated contexts (no token explosion)
- Composable results (easy to integrate)
- Clear responsibility separation

### Deployment Models

**1. Ephemeral Containers (One-Off Tasks)**

```
User Request → Create Container → Run Agent → Container Destroyed
```

Best for:
- Single tasks
- One-off requests
- User-initiated work

Providers: AWS Lambda, Google Cloud Run, Azure Functions

**2. Persistent Containers (Long-Running Agents)**

```
Keep Container Running → Multiple Agent Instances → Background Processing
```

Best for:
- Proactive agents
- Content processing
- High-message-volume handling

Providers: AWS EC2, Google Cloud VMs, custom Kubernetes

**3. Hydrated Ephemeral (Resumable Work)**

```
Container + Session History → Resume Work → Return Results
```

Best for:
- Intermittent user interaction
- Work that spans sessions
- Preserve history between runs

Implementation: Load previous session state before starting

**4. Multi-Agent Shared Container**

```
Single Container → Multiple Agent Instances → Shared Filesystem
```

Best for:
- Agents working on same project
- Tight coordination needed
- Shared resource management

Caution: Must prevent agents from overwriting each other

---

## Antigravity IDE Integration

### What is Antigravity?

**What:** Google's new agentic development IDE  
**Release:** November 2025  
**Key Features:**
1. Agent Manager & Editor Shared Workflows
2. Agentic Inbox for tracking parallel tasks
3. Browser Agent for automated testing/debugging

### How Claude Code Integrates with Antigravity

**Architecture:**

```
┌─────────────────────────────────────────────────────┐
│         ANTIGRAVITY IDE (Google)                    │
│                                                     │
│  Gemini 3 Pro           │        Claude Code       │
│  (Planning Agent)       │        (Execution Agent)  │
│  ├─ Research          │        ├─ Code generation │
│  ├─ Architecture      │        ├─ File editing    │
│  └─ Documentation     │        └─ Testing         │
│                                                     │
│  Agent Manager → Coordinates both agents           │
│  Shared Workspace → Common file system             │
│  Agentic Inbox → Task tracking                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Recommended Workflow: Hybrid Approach

**Phase 1: Planning (Gemini 3 Pro)**
- Analyze requirements
- Research solutions
- Create architecture document
- Estimate complexity

```
User: "Build an RSS reader app with authentication"
Gemini 3 Pro:
├─ Analyzes requirements
├─ Creates architecture.md
├─ Lists dependencies
└─ Generates project structure
```

**Phase 2: Execution (Claude Code)**
- Reference architecture from Phase 1
- Generate code
- Implement features
- Manage file edits

```
User: "Use the architecture from Gemini, build it with Claude"
Claude Code:
├─ Reads architecture.md
├─ Generates scaffolding
├─ Implements components
└─ Manages dependencies
```

**Phase 3: Testing (Antigravity Browser Agent)**
- Automated testing
- Visual verification
- Debugging
- Refinement

```
Browser Agent:
├─ Tests authentication flow
├─ Verifies RSS feeds load
├─ Captures screenshots
└─ Reports issues back to Claude
```

**Phase 4: Deployment**
- Deploy to staging/production
- Verify in live environment

### Token Efficiency Strategy

**Problem:** Each tool (Gemini, Claude, Testsprite) has usage limits.

**Solution:** Specialized workflows

| Agent | Best For | Token Budget |
|-------|----------|--------------|
| **Gemini 3 Pro** | Planning, architecture, research | High (free tier) |
| **Claude Code** | Actual coding, file operations | Moderate (paid) |
| **Testsprite MCP** | Testing/verification | Low (specific tests) |

**Implementation:**

1. **Let Gemini Plan** - Creates architecture document
2. **Claude References Plan** - No need to re-research
3. **Use Testsprite for Testing** - Verifies without manual testing
4. **Avoid Duplication** - Share context across tools

### Setup Instructions for Antigravity + Claude Code

**Step 1: Install Claude Code Extension**

```
Antigravity Extensions → Search "Claude Code" 
→ Install "Claude Code for VS Code"
```

**Step 2: Configure API Keys**

```
Settings → Extensions → Claude Code → Configure API Key
Paste your Anthropic API key
```

**Step 3: Create Terminal Session**

```bash
# In Antigravity terminal
cd your-project
claude

# Claude agent spawns in terminal
# Full access to project files and bash commands
```

**Step 4: Connect MCP Tools (Optional)**

```json
// In .claude/config.json (if supported)
{
  "mcpServers": {
    "testsprite": {
      "command": "mcp-testsprite",
      "args": ["--config", "testsprite.json"]
    }
  }
}
```

Then use in Claude:
```
@testsprite run tests for my-component
```

### Real-World Antigravity + Claude Code Workflow

**Example: Building Landing Page**

1. **Gemini Planning Phase (5-10 min)**
   - Input: "Build a landing page for AI Profit Boardroom"
   - Gemini creates: design specs, layout plan, component list
   - Output: design-spec.md

2. **Claude Execution Phase (15-30 min)**
   - Input: Read design-spec.md → Build landing page
   - Claude creates: HTML/CSS/JS components
   - Output: index.html, components/, styles/

3. **Verification**
   - Take screenshot of rendered page
   - Verify against design spec
   - Iterate on styling/layout

4. **Refinement**
   - "Fix the spacing on the features section"
   - Claude applies targeted edits
   - Verify with screenshot

### Integration Considerations

**Context Passing Between Tools**

```
Gemini creates: roadmap.md
    ↓
Claude reads: cat roadmap.md
    ↓
Claude codes based on plan (no re-planning needed)
    ↓
Saves 50-70% of Claude tokens
```

**File Organization for Multi-Agent Work**

```
project/
├── PLANNING.md          # From Gemini
│   ├─ Architecture
│   ├─ Component specs
│   └─ Dependencies
├── src/
│   └─ Components built by Claude
├── tests/
│   └─ Test specs from Testsprite
└── claude-progress.txt  # Agent progress tracking
```

**Agent Switching Decision Tree**

```
Task: "Build app with auth, test it, deploy"

Is it planning/architecture? → Use Gemini
    ↓ (save results)
Is it coding/implementation? → Use Claude Code
    ↓ (save code)
Is it testing/verification? → Use Testsprite
    ↓ (save results)
Is it deployment? → Use Antigravity's deployment features
```

---

## Best Practices & Design Principles

### 1. Simplicity First

**Principle:** Start simple, add complexity only when it demonstrably improves results.

**Hierarchy of Complexity:**

```
1. Single LLM call with good prompt
   ↓ (if not sufficient)
2. LLM + tools + retrieval
   ↓ (if not sufficient)
3. Prompt chaining (multi-step workflow)
   ↓ (if not sufficient)
4. Agent (iterative, autonomous)
   ↓ (if not sufficient)
5. Multi-agent system (orchestration)
```

**Measurement:** Always A/B test. Only move to next level if metrics improve.

### 2. Transparency in Agent Decision-Making

**Requirement:** Users must understand WHY the agent is taking an action.

**Implementation:**

```python
# Show agent reasoning
print("AGENT REASONING:")
print(f"- User asked for: {user_request}")
print(f"- I identified these sub-tasks: {subtasks}")
print(f"- I'm using tools: {chosen_tools}")
print(f"- Here's my plan: {execution_plan}")

# Then execute with visibility
print("\nEXECUTION:")
for step in execution_steps:
    print(f"- {step.action}")
    print(f"  Result: {step.result}")
```

**Why:** Builds trust, enables debugging, helps detect agent errors before they propagate.

### 3. Tool Design as Critical Path

**Insight:** Tool design impacts agent performance as much as the agent prompt itself.

**Spend time on:**
- Clear parameter names and descriptions
- Comprehensive examples
- Edge case handling
- Error message clarity
- Input validation

**Anti-patterns:**
- Too many tools (agent gets confused)
- Vague descriptions
- Inconsistent naming conventions
- Missing examples

### 4. Structured Output for Verification

**Principle:** Make verification deterministic, not fuzzy.

**Approach:**

```python
# Bad: Fuzzy evaluation
"Did the agent do a good job?"  # Subjective

# Good: Structured rules
{
    "requirements_met": ["auth", "database", "api"],
    "code_quality": {
        "passes_linting": true,
        "has_tests": true,
        "documentation_complete": true
    },
    "performance": {
        "load_time_ms": 340,
        "memory_mb": 45
    }
}
```

Rules-based feedback is always better than LLM-as-judge when possible.

### 5. Iterative Development

**Process:**

1. Define clear success criteria
2. Run agent on representative test cases
3. Analyze failures (don't just log them)
4. Improve based on failure patterns
5. Measure improvement
6. Repeat

**Tools for iteration:**
- Programmatic evaluation (evals)
- Test case libraries
- Failure analysis
- Metrics tracking

### 6. Context Engineering

**Principle:** How you structure information available to the agent dramatically impacts performance.

**Techniques:**

```python
# Technique 1: Agentic search (agent navigates)
agent.bash("ls -la src/")
agent.bash("grep -r 'function_name' src/")

# Technique 2: Progressive loading (start minimal)
# SKILL.md is small, reference.md loaded only when needed

# Technique 3: Subagents (isolation)
# Give each subagent only relevant context

# Technique 4: Filesystem structure as context
# Organize files so ls/find provide useful context
project/
├── PRIORITY_FEATURES.md  # Agent reads first
├── src/
│   ├── auth/            # Agent knows where auth code is
│   ├── api/
│   └── database/
└── docs/
    └── api_reference.md  # Agent loads when implementing API
```

---

## Implementation Checklist

### Phase 1: Define Agent Scope

- [ ] Clearly articulate what the agent should accomplish
- [ ] Identify success criteria (measurable outcomes)
- [ ] Define boundaries and constraints
- [ ] List required integrations and data sources
- [ ] Determine approval/oversight requirements

### Phase 2: Design Agent Components

**Tools & Actions:**
- [ ] List 5-15 primary tools agent will use
- [ ] Design tool parameters and return types
- [ ] Write detailed tool descriptions with examples
- [ ] Plan error handling and edge cases
- [ ] Design feedback mechanisms

**Gathering Context:**
- [ ] Plan file/data organization for agentic search
- [ ] Decide if semantic search needed
- [ ] Plan subagent architecture (if applicable)
- [ ] Design memory/progress tracking

**Verification:**
- [ ] Define success rules (linting, validation, etc.)
- [ ] Plan visual feedback (if applicable)
- [ ] Design error recovery flows

### Phase 3: Implement Core Agent

- [ ] Set up development environment
- [ ] Implement agent loop (gather → act → verify)
- [ ] Integrate tools (start with 3-5 most important)
- [ ] Add basic error handling
- [ ] Create test harness

### Phase 4: Add Intelligence Components

**If using Agent Skills:**
- [ ] Identify domain-specific workflows
- [ ] Create SKILL.md for first skill
- [ ] Add examples and references as needed
- [ ] Integrate into agent
- [ ] Test skill discovery and loading

**If using MCP:**
- [ ] Identify external integrations needed
- [ ] Select or build MCP servers
- [ ] Integrate with agent
- [ ] Test tool discovery and execution
- [ ] Set up authentication/authorization

### Phase 5: Optimization & Testing

- [ ] Create test case library (20-50 representative cases)
- [ ] Run agent on test cases
- [ ] Analyze failures and identify patterns
- [ ] Improve tools/skills based on patterns
- [ ] Measure improvement with metrics
- [ ] Iterate (Steps 4-5)

### Phase 6: Deployment

- [ ] Choose deployment model (ephemeral/persistent/hydrated)
- [ ] Set up sandboxed environment
- [ ] Configure resource limits
- [ ] Set up logging and monitoring
- [ ] Plan rollout strategy
- [ ] Set up user feedback mechanisms

### Phase 7: Maintenance

- [ ] Monitor agent performance
- [ ] Track failure patterns
- [ ] Update tools based on usage
- [ ] Manage Skills/MCP servers
- [ ] Plan capacity and scaling
- [ ] Security audits

---

## Security & Deployment

### Sandboxing Requirements

**Essential for Production:**

1. **Container Isolation**
   - Use Docker/gVisor/Firecracker
   - Process isolation
   - Filesystem isolation

2. **Resource Limits**
   - CPU: Set hard limits
   - Memory: Monitor and cap
   - Disk: Ephemeral or limited capacity
   - Network: Whitelist allowed domains

3. **Network Control**
   - Only allow API calls to whitelisted endpoints
   - Block outbound by default
   - Implement rate limiting

4. **Credential Management**
   - Never store credentials in code
   - Use environment variables
   - Rotate credentials regularly
   - Audit access logs

### Security Best Practices

**1. Tool Input Validation**

```python
@agent.tool()
async def delete_file(filepath: str) -> str:
    # Validate before execution
    if not is_safe_path(filepath):
        raise ValueError(f"Access denied to {filepath}")
    
    if not filepath.startswith("/allowed/directory/"):
        raise ValueError("Only files in allowed directory can be deleted")
    
    os.remove(filepath)
    return "File deleted"
```

**2. Skill Auditing**

Before using any skill:
- [ ] Review all files in skill directory
- [ ] Check for suspicious code
- [ ] Verify external network calls
- [ ] Check file access patterns
- [ ] Audit dependencies

**3. MCP Server Validation**

When using MCP servers:
- [ ] Use official servers from modelcontextprotocol.io when possible
- [ ] Audit third-party MCP servers thoroughly
- [ ] Verify authentication implementation
- [ ] Test rate limiting and error handling
- [ ] Monitor data access logs

**4. Monitoring & Alerting**

```python
# Log all significant agent actions
logging.info(f"AGENT ACTION: {agent_id} called {tool_name}")
logging.info(f"TOOL RESULT: {result}")

# Alert on suspicious patterns
if failed_attempts > 5:
    alert("Too many tool failures", severity="medium")

if unusual_file_access:
    alert("Unusual file access pattern", severity="high")

if external_api_failed:
    alert("External API failure", severity="medium")
```

### Deployment Cost Considerations

**Primary Cost Driver:** Token consumption

**Typical costs:**

- Container instance: ~$0.05/hour idle
- Tokens: ~$3-15 per million tokens
- Agent session: $0.50-5 depending on task complexity

**Cost Optimization:**

1. **Use smaller models for subagents:** Claude Haiku for simple tasks
2. **Implement context compaction:** Summarize old context
3. **Design efficient tools:** Reduce tokens needed per tool call
4. **Plan token budgets:** Set max_tokens per session
5. **Batch operations:** Combine multiple requests

---

## Recommended Resources

### Official Documentation

**Anthropic:**
- https://www.anthropic.com/research/building-effective-agents
- https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://platform.claude.com/docs/en/agent-sdk/overview

**Model Context Protocol:**
- https://modelcontextprotocol.io
- https://modelcontextprotocol.io/docs/learn/architecture
- https://modelcontextprotocol.io/docs/develop/build-server

**Claude API:**
- https://platform.claude.com/docs/
- https://github.com/anthropics/skills

### Community Resources

- YouTube: "Claude Agent SDK Full Workshop" - Thariq Shihipar (Anthropic)
- GitHub: https://github.com/anthropics/skills (examples)
- GitHub: https://github.com/modelcontextprotocol (MCP implementations)

### For Antigravity Integration

- https://antigravity.google/
- YouTube: "Antigravity + Claude Code" tutorials
- Blog: https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/

---

## Conclusion

Anthropic's agent frameworks represent a maturation of the agentic AI space. Key takeaways:

1. **Start Simple** - Build with basic components, add complexity only when needed
2. **Use MCP for Integration** - Standardize external tool connections
3. **Leverage Agent Skills** - Encapsulate domain expertise reusably
4. **Employ Agent SDK** - Use production-tested patterns for agent harness
5. **Transparent Reasoning** - Always show agent's thinking
6. **Verify Systematically** - Use rules-based feedback, not fuzzy judgment
7. **Manage Context Carefully** - Long-running agents need memory architecture
8. **Secure by Default** - Sandbox all agent execution

For Antigravity IDE specifically: Use hybrid workflows (Gemini for planning, Claude for coding, specialized tools for testing) to maximize efficiency and minimize token usage.

The future of agents isn't about building more complex systems—it's about building more efficient, transparent, and reliable ones. These frameworks provide the foundation.

---

**Document Version:** 1.0  
**Last Updated:** January 7, 2026  
**Curated by:** AI Research & Engineering Division  
**Next Update:** Expected Q1 2026 with SDK improvements
