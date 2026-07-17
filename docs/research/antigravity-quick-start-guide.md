# Antigravity IDE + Claude Agent Integration: Quick Start Guide

**Version:** 1.0  
**Created:** January 7, 2026  
**Audience:** AI/Automation Entrepreneurs using Antigravity IDE

---

## Executive Overview

This guide provides a practical, step-by-step approach to integrating Claude Agent capabilities into your Antigravity IDE workflows for optimal automation.

**Key Insight:** Antigravity + Claude Code + Specialized Tools = Maximum Efficiency with Minimum Token Spend

---

## Architecture: The Optimal Stack

```
┌─────────────────────────────────────────────────────────────┐
│              ANTIGRAVITY AGENT STACK                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: PLANNING (Gemini 3 Pro - Free)                   │
│  ├─ Architecture design                                    │
│  ├─ Requirements analysis                                  │
│  ├─ Research & documentation                              │
│  └─ Save outputs → architecture.md                        │
│                                                             │
│  Layer 2: EXECUTION (Claude Code - Paid)                   │
│  ├─ Code generation                                        │
│  ├─ File management                                        │
│  ├─ Component implementation                               │
│  └─ Reference architecture.md (no re-planning)             │
│                                                             │
│  Layer 3: TESTING (Testsprite MCP - Per-test)              │
│  ├─ Automated test generation                              │
│  ├─ Test execution                                         │
│  ├─ Verification reports                                   │
│  └─ Save results → test-results.md                         │
│                                                             │
│  Layer 4: ITERATION (Claude Code - Paid)                   │
│  ├─ Fix failures                                           │
│  ├─ Optimize performance                                   │
│  ├─ Update documentation                                   │
│  └─ Reference test-results.md for context                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Token Flow:
• Planning: ~10,000-20,000 tokens (once per project)
• Execution: ~5,000-50,000 tokens (main implementation)
• Testing: ~2,000-10,000 tokens (verification)
• Iteration: ~2,000-10,000 tokens (per refinement)

TOTAL SAVED vs. Single Agent: 50-70% token reduction
```

---

## Step 1: Project Setup in Antigravity

### 1.1 Initialize Project Structure

```bash
mkdir my-project
cd my-project

# Create key planning documents
touch REQUIREMENTS.md
touch ARCHITECTURE.md
touch PROGRESS.md
```

### 1.2 Create Shared Context File

```bash
# This file is read by both Gemini and Claude
cat > PROJECT_BRIEF.md << 'EOF'
# Project Brief

## Objective
[Your project goal]

## Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Success Criteria
- [Criterion 1]
- [Criterion 2]

## Tech Stack
- [Technology 1]
- [Technology 2]
EOF
```

---

## Step 2: Phase 1 - Planning with Gemini 3 Pro

### 2.1 Prompt Gemini for Architecture

Open Antigravity → Chat → Gemini 3 Pro

**Prompt:**
```
Read PROJECT_BRIEF.md and create a detailed implementation plan.

Provide:
1. System architecture diagram (ASCII)
2. File structure
3. Component specifications
4. Dependency list
5. Implementation order
6. Estimated complexity per component

Save as ARCHITECTURE.md
```

**Expected Output:**
```
ARCHITECTURE.md contains:
├─ Architecture diagram (ASCII format)
├─ File structure (with descriptions)
├─ Component specs (name, purpose, inputs/outputs)
├─ Dependencies list (libraries, services)
├─ Implementation order (Phase 1, 2, 3...)
└─ Complexity assessment (Easy/Medium/Hard)
```

### 2.2 Generate Research Documentation (Optional)

**Prompt:**
```
Create a RESEARCH.md file documenting:
1. Best practices for [technology]
2. Common pitfalls and how to avoid them
3. Performance optimization tips
4. Security considerations
5. Testing strategies

Keep it concise (2-3k tokens)
```

**Token Cost:** 10-20k tokens for full planning (one-time per project)

**Result:** Complete documentation that Claude can reference without re-doing research.

---

## Step 3: Phase 2 - Execution with Claude Code

### 3.1 Install Claude Code Extension in Antigravity

```
Antigravity → Extensions → Search "Claude Code"
→ Install "Claude Code for VS Code"
```

### 3.2 Configure Claude in Terminal

```bash
# In Antigravity terminal
cd your-project

# Start Claude agent
claude

# Expected: Claude spawns in terminal with full project access
```

### 3.3 Prime Claude with Architecture

**First Message to Claude:**

```
You are building the following project. Read these files for context:
- PROJECT_BRIEF.md (requirements)
- ARCHITECTURE.md (design)

Do NOT re-research these topics. Use the documentation provided.

Your task: Implement Phase 1 of the architecture
(See ARCHITECTURE.md for implementation order)

When complete:
1. Update PROGRESS.md with what you accomplished
2. Leave code clear and commented
3. Highlight any issues or ambiguities
```

**Why This Works:**
- Claude reads existing documentation (saved tokens)
- Clear phase-by-phase breakdown (prevents task creep)
- Progress tracking for future sessions

### 3.4 Manage Phase Implementation

**For Each Phase:**

```
User: "Review ARCHITECTURE.md Phase 1. Build [component]."

Claude:
├─ Reads ARCHITECTURE.md
├─ Implements component
├─ Runs basic tests (linting, etc.)
├─ Updates PROGRESS.md
└─ Reports completion + issues

Token Cost: 5-15k per phase (depending on complexity)
```

### 3.5 Review & Approve

**Interactive Approval Pattern:**

```
Claude: "I've implemented the authentication system. 
Here's what I did: [summary]

Shall I proceed to the next phase?"

You: "Good work! One question about the password hashing. 
Can you switch from bcrypt to argon2 for better security?"

Claude: Updates code, re-tests, reports ready for next phase
```

**Token Cost Per Iteration:** 2-5k tokens (targeted improvements)

---

## Step 4: Phase 3 - Testing with Testsprite MCP (Optional)

### 4.1 Connect Testsprite MCP

If your Antigravity setup supports MCP:

```json
// In .claude/config.json or similar
{
  "mcpServers": {
    "testsprite": {
      "command": "mcp-testsprite",
      "config": "testsprite.json"
    }
  }
}
```

### 4.2 Generate & Run Tests

**Prompt to Claude:**

```
Using the Testsprite MCP tool, create tests for:
1. Authentication system (login, logout, token refresh)
2. API endpoints (CRUD operations)
3. Error handling (invalid inputs, edge cases)

Run the tests and provide results in TEST_RESULTS.md
```

**Expected Output:**
```
TEST_RESULTS.md:
├─ Test summary (passed/failed counts)
├─ Failed test details
├─ Performance metrics
├─ Coverage report
└─ Recommendations
```

**Token Cost:** 2-5k tokens (depends on test complexity)

---

## Step 5: Phase 4 - Iteration & Refinement

### 5.1 Read Test Results

```
Claude reads TEST_RESULTS.md

Claude: "I see 3 test failures:
1. Authentication timeout (expected vs actual)
2. API rate limiting not enforced
3. Error message clarity

Shall I fix these?"
```

### 5.2 Targeted Fixes

**Prompt:**
```
Fix the failures documented in TEST_RESULTS.md.
Reference the failures and show fixes inline.

After changes, re-run tests and update TEST_RESULTS.md.
```

**Workflow:**
```
Test Failure → Claude Reads Report → Claude Fixes → Re-Test → Report
```

**Token Cost:** 2-10k per iteration (usually 1-3 iterations needed)

---

## Complete Example: Building an API Agent

### Project: "Lead Capture & Email Automation Agent"

**Step 1: Planning (15 min)**

```bash
# Create PROJECT_BRIEF.md
Objective: Build autonomous agent that captures leads from LinkedIn, enriches data, sends personalized emails

Requirements:
- Scrape LinkedIn using n8n/Apify
- Enrich with email finder API
- Store in MongoDB
- Send via Gmail API with personalization
- Track opens/clicks via Zapier

Tech Stack:
- Backend: Node.js + Express
- Database: MongoDB
- Automations: n8n
- APIs: LinkedIn, Email Finder, Gmail, Zapier
```

**Prompt to Gemini:**
```
Read PROJECT_BRIEF.md and create ARCHITECTURE.md with:
1. System components diagram
2. API flow
3. Database schema
4. Implementation phases (Frontend/Backend/Integration)
5. Security considerations
```

**Gemini Output (10-15k tokens):**
```
ARCHITECTURE.md created with:
├─ Component architecture
├─ Data flow diagrams
├─ Database schema (Users, Leads, Emails, Tracking)
├─ API endpoints list
├─ Phase breakdown:
│  ├─ Phase 1: Database + Core APIs
│  ├─ Phase 2: Email automation
│  └─ Phase 3: Tracking & Analytics
└─ Security notes
```

**Step 2: Execution (2-3 hours)**

**Phase 1 Prompt to Claude:**
```
Read ARCHITECTURE.md Phase 1.

Implement:
1. MongoDB schemas (Users, Leads, Emails)
2. Express API endpoints (CRUD for leads)
3. Basic authentication (JWT tokens)
4. Environment variable setup

Reference ARCHITECTURE.md. Do not re-research MongoDB best practices.
```

**Claude Work:**
- Reads ARCHITECTURE.md (saved tokens)
- Creates models/
- Creates routes/
- Implements auth
- Tests endpoints
- Updates PROGRESS.md

**Token Cost:** 8-12k tokens

**Phase 2 & 3:**
Similar pattern, each ~10-15k tokens.

**Step 3: Testing (Optional)**

```
Prompt to Claude (with Testsprite MCP):

Create tests for:
- Authentication flow
- Lead CRUD operations
- Email dispatch
- Error handling

Use Testsprite for automated testing.
```

**Step 4: Refinement**

```
Claude reads test failures from TEST_RESULTS.md

Fixes identified issues:
- Add input validation
- Improve error messages
- Handle edge cases

Re-test and verify.
```

**Final Token Usage:**
- Planning: 15k (one-time)
- Phase 1-3: 30-40k total
- Testing: 5-10k
- Iteration: 5-10k
- **TOTAL: ~55-75k tokens**

**Savings:** vs. having Claude do everything (would be 150-200k)

---

## Best Practices for Antigravity + Claude

### 1. Always Document Before Coding

```
❌ Bad: "Build a user authentication system"
✅ Good: Read ARCHITECTURE.md, then "Implement Phase 2.1: User authentication"
```

**Why:** Reduces tokens, prevents re-planning, keeps Claude focused.

### 2. Use Phase-Based Approach

```
ARCHITECTURE.md
├─ Phase 1: Foundations (DB, Auth, Core APIs)
├─ Phase 2: Features (Main functionality)
└─ Phase 3: Polish (Testing, optimization, deployment)

Each phase is separate Claude conversation/session.
Saves 30-40% tokens vs. building everything at once.
```

### 3. Leverage File System as Context

```
project/
├── ARCHITECTURE.md      ← Claude reads before starting
├── PROGRESS.md          ← Updated after each phase
├── src/
│   ├── api/
│   ├── database/
│   └── utils/
└── TEST_RESULTS.md      ← Claude reads for iteration
```

**Pattern:** File system IS the agent's memory system.

### 4. Use MCP for Integrations

```
# Instead of Claude manually calling APIs:
✅ Use MCP servers:
   ├─ Slack MCP (if you need Slack integration)
   ├─ GitHub MCP (if you need GitHub operations)
   └─ Testsprite MCP (for automated testing)

MCP handles auth, API calls, reducing token load.
```

### 5. Interactive Approval Loop

```
After each deliverable:
1. Claude presents summary of work
2. You ask for modifications (if needed)
3. Claude makes targeted changes
4. Move to next phase

This keeps you in control and prevents wrong directions.
```

### 6. Token Budget Per Phase

```
For a typical API project:

Phase 1 (DB + Auth): 8-12k tokens
Phase 2 (Features): 10-20k tokens
Phase 3 (Integration): 8-15k tokens
Phase 4 (Testing): 5-10k tokens
Iteration/Fixes: 5-10k tokens

Total: ~40-65k tokens per project
```

---

## Common Issues & Solutions

### Issue 1: Claude Re-researching Topics

**Problem:**
```
You: "Implement authentication"
Claude: "I'll implement JWT tokens. Let me research JWT best practices..."
```

**Solution:**
```
ARCHITECTURE.md should include:
## Authentication

We're using JWT tokens with:
- Expiry: 24 hours
- Secret: Stored in environment variables
- Refresh tokens: Redis-based

Reference this section.
```

**Prompt Fix:**
```
"Review the authentication section in ARCHITECTURE.md. 
Implement exactly as specified. Don't research alternatives."
```

### Issue 2: Claude Getting Lost in Large Projects

**Problem:**
```
Claude tries to implement everything at once and gets confused.
```

**Solution:**
```
Always use phases and reference ARCHITECTURE.md.

Prompt: "You're building Phase 1 only. 
See ARCHITECTURE.md Phase 1 for what's included.
Do not implement Phase 2 components."
```

### Issue 3: Token Creep During Iteration

**Problem:**
```
Each iteration costs more tokens because context grows.
```

**Solution:**
```
Use session-based approach:
1. End Claude session after each phase (saves old context)
2. New session reads PROGRESS.md (summary, not full history)
3. Start fresh for next phase

Token savings: 20-30% per iteration.
```

### Issue 4: Unclear Requirements

**Problem:**
```
Claude asks too many clarifying questions.
```

**Solution:**
```
Make PROJECT_BRIEF.md and ARCHITECTURE.md very specific.

Include:
- Tech stack decisions (with why)
- Architecture diagrams (ASCII or links)
- Specific API versions (not "latest")
- Security requirements
- Performance targets

Leave less room for ambiguity.
```

---

## Advanced: Multi-Agent Workflows

### Scenario: Large Build with Multiple Specialists

```
PLAN (Gemini):
├─ Architecture
├─ Database design
└─ API specification

            ↓

BUILD (Claude Code):
├─ Backend APIs
├─ Database models
└─ Authentication

            ↓

TEST (Testsprite MCP):
├─ Unit tests
├─ Integration tests
└─ E2E tests

            ↓

FRONTEND (Claude Code):
├─ React components
├─ State management
└─ API integration

            ↓

DEPLOY (Antigravity):
├─ Docker setup
├─ CI/CD config
└─ Monitoring
```

**Token Efficiency:**
- No duplication of work
- Each agent focuses on specialization
- Clear handoff documentation
- Total: 70-100k tokens for large project

---

## Monitoring & Optimization

### Track Metrics

```json
{
  "project": "lead-capture-agent",
  "tokens_used": {
    "planning": 15000,
    "implementation_phase1": 12000,
    "implementation_phase2": 14000,
    "testing": 8000,
    "iteration": 6000,
    "total": 55000
  },
  "time_spent": {
    "planning": "15 minutes",
    "implementation": "2 hours",
    "testing": "30 minutes",
    "iteration": "20 minutes",
    "total": "3 hours 5 minutes"
  },
  "efficiency": {
    "tokens_per_hour": 18000,
    "estimated_cost": "$0.27"
  }
}
```

### Optimization Targets

- **Reduce redundant documentation:** 1-time research vs. per-phase
- **Clear phase boundaries:** Prevents scope creep
- **Use MCP for integrations:** Saves custom API handling tokens
- **Session management:** Clear separation = context reduction
- **Structured error handling:** Reduces iteration cycles

---

## Your Automation Startup: Using This Framework

### How This Applies to Your Business

**Your Use Case:** Building AI automation agencies + fractional CFO services

**Optimization Strategy:**

```
For Each Client Project:

1. PLANNING PHASE (Gemini)
   └─ Analyze client requirements
   └─ Create SOW (Statement of Work)
   └─ Document architecture
   └─ Cost: $0.10-0.30 per project

2. IMPLEMENTATION PHASE (Claude Code)
   └─ Build automations based on architecture
   └─ Integrate with client APIs (MCP)
   └─ Set up n8n/Apify workflows
   └─ Cost: $0.50-2.00 per project

3. TESTING PHASE (Testsprite MCP)
   └─ Verify data accuracy
   └─ Test edge cases
   └─ Validate integrations
   └─ Cost: $0.10-0.30 per project

4. DELIVERY PHASE (Antigravity)
   └─ Documentation
   └─ Training materials
   └─ Handoff to client
   └─ Cost: Minimal (mostly CLI/docs)

TOTAL COST PER PROJECT: $0.70-2.60
CHARGE CLIENT: $3,000-10,000
PROFIT MARGIN: 1,154-14,186%
```

**Scaling Strategy:**

```
Month 1: 3 projects = $50k revenue
Month 2: 6 projects = $100k revenue
Month 3: 12 projects = $200k revenue
Month 4: Hire first person to handle operations

With this framework:
- Each project uses 50-80k tokens max
- Cost per project: ~$0.50-1.50
- 20-50 projects/month at full scale
- Gross margin: 95%+
```

---

## Checklist: Before You Start a Project

- [ ] Create PROJECT_BRIEF.md with clear requirements
- [ ] Run planning phase with Gemini (save ARCHITECTURE.md)
- [ ] Claude reads ARCHITECTURE.md before starting
- [ ] Phase-based implementation (not everything at once)
- [ ] Update PROGRESS.md after each phase
- [ ] Use MCP for external integrations
- [ ] Document all API keys/configs in environment
- [ ] Test using Testsprite MCP or similar
- [ ] Read test results before iteration
- [ ] Save final project structure + documentation
- [ ] Track token usage and timing

---

## Resources Used in This Guide

1. https://www.anthropic.com/research/building-effective-agents
2. https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
3. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
4. https://modelcontextprotocol.io/docs/learn/architecture
5. https://platform.claude.com/docs/en/agent-sdk/overview
6. https://antigravity.google/
7. https://www.youtube.com/watch?v=yMJcHcCbgi4 (Antigravity + Claude Code)

---

**Version:** 1.0  
**Last Updated:** January 7, 2026  
**Audience:** Automation Entrepreneurs & Technical Founders  
**Next Review:** April 2026 (when Claude Agent SDK v2 expected)
