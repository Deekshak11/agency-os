# Quick Reference: Official Documentation URLs & Resources

**Document Version:** 1.0  
**Created:** January 7, 2026  
**Purpose:** Direct access to all official frameworks documentation

---

## 🎯 Primary Documentation Links

### Anthropic Official Resources

#### Building Effective Agents (Foundational)
- **URL:** https://www.anthropic.com/research/building-effective-agents
- **Focus:** Core principles, when to use agents vs. workflows, prompt chaining, routing, parallelization patterns
- **Read Time:** 20-30 minutes
- **Key Takeaway:** Start simple, only increase complexity when it measurably improves results

#### Building Agents with Claude Agent SDK
- **URL:** https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
- **Focus:** Agent loop (gather → act → verify), context gathering, tools, MCP integration, verification strategies
- **Read Time:** 25-35 minutes
- **Key Takeaway:** Complete agent harness architecture from 6+ months of Claude Code production experience

#### Equipping Agents for the Real World with Agent Skills
- **URL:** https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Focus:** Progressive disclosure, SKILL.md structure, filesystem-based architecture, development best practices
- **Read Time:** 20-25 minutes
- **Key Takeaway:** Package domain expertise as reusable, dynamically-loadable skills

#### Effective Harnesses for Long-Running Agents
- **URL:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **Focus:** Context management across sessions, initializer pattern, claude-progress.txt, git-based tracking
- **Read Time:** 15-20 minutes
- **Key Takeaway:** Multi-session architecture with proper initialization and state tracking

#### Code Execution with MCP
- **URL:** https://www.anthropic.com/engineering/code-execution-with-mcp
- **Focus:** Using MCP for code execution, standardized integrations, performance improvements
- **Read Time:** 10-15 minutes

### Claude API Documentation

#### Agent Skills Overview
- **URL:** https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- **Focus:** Technical implementation, API usage, pre-built skills, custom skill creation
- **Status:** Latest (December 2025)

#### Agent SDK Overview
- **URL:** https://platform.claude.com/docs/en/agent-sdk/overview
- **Focus:** SDK architecture, capabilities, comparison with client SDK
- **Status:** Production-ready

#### Agent SDK Hosting & Deployment
- **URL:** https://platform.claude.com/docs/en/agent-sdk/hosting
- **Focus:** Container strategies (ephemeral, persistent, hydrated), cost optimization, scaling
- **Read Time:** 15-20 minutes

---

## 🔌 Model Context Protocol (MCP) Resources

### Official MCP Documentation

#### Architecture Overview
- **URL:** https://modelcontextprotocol.io/docs/learn/architecture
- **Focus:** Client-server architecture, layers (data & transport), lifecycle management, primitives
- **Read Time:** 20-25 minutes
- **Key Sections:**
  - MCP Host, Client, Server participants
  - Data vs. Transport layers
  - Tools, Resources, Prompts primitives
  - Initialization sequence with JSON-RPC examples
  - Real-time notifications

#### Build an MCP Server
- **URL:** https://modelcontextprotocol.io/docs/develop/build-server
- **Focus:** Practical implementation in Python, tool execution, testing with Claude Desktop
- **Read Time:** 30-40 minutes (hands-on)
- **Includes:** Complete weather API example with NWS integration

#### MCP Specification & SDKs
- **URL:** https://modelcontextprotocol.io
- **Focus:** Complete specification, SDK downloads (Python, TypeScript, C#, Java)
- **Repository:** https://github.com/modelcontextprotocol

### Community MCP Guides

#### MCP Servers in 2025: Beginner's Guide
- **URL:** https://superagi.com/mastering-mcp-servers-in-2025-a-beginners-guide-to-model-context-protocol-implementation/
- **Focus:** Hardware requirements, installation, configuration, security, performance optimization
- **Read Time:** 25-30 minutes

#### The Complete MCP Guide for Developers
- **URL:** https://dev.to/kevinz103/the-complete-mcp-guide-for-developers2025-edition-ana
- **Focus:** Developer-focused implementation guide for 2025

#### Build an MCP Server in Minutes
- **URL:** https://www.gravitee.io/blog/mcp-server-explained
- **Focus:** Practical, quick-start approach to MCP server development

#### The Definitive Guide to MCP
- **URL:** https://datasciencedojo.com/blog/guide-to-model-context-protocol/
- **Focus:** Comprehensive overview with practical examples

---

## 🤖 Agent Skills Resources

### Official Skills Documentation

#### Agent Skills Overview (Full Docs)
- **URL:** https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- **Contains:** SKILL.md structure, progressive disclosure, API usage, pre-built skills list

### Skills Examples & Cookbook

#### Official Skills Repository
- **URL:** https://github.com/anthropics/skills
- **Contains:** Production examples, complete SKILL.md files, best practices

---

## 🚀 Claude Agent SDK Resources

### Complete SDK Architecture Deep Dive

#### Claude Agent SDK Full Workshop
- **URL:** https://www.youtube.com/watch?v=TqC1qOfiVcQ
- **Duration:** ~100 minutes (filmed Jan 2026)
- **Speaker:** Thariq Shihipar (Anthropic)
- **Covers:**
  - Agent definition and philosophy
  - Harness architecture (tools, prompts, skills, subagents)
  - Agent loop implementation
  - Context engineering
  - Multi-turn complex tasks
  - Reproducibility and scaling
  - Q&A on real-world challenges

### SDK Installation & Getting Started

#### Claude Agent SDK GitHub
- **URL:** https://github.com/anthropics/claude-agent-sdk
- **Contains:** Latest SDK code, examples, quickstart guide

#### NPM Package
- **URL:** https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk
- **Installation:** `npm install -g @anthropic-ai/claude-agent-sdk`

---

## 🌐 Antigravity IDE Integration

### Google Antigravity Resources

#### Official Antigravity Blog
- **URL:** https://antigravity.google/blog/introducing-google-antigravity
- **Focus:** Features, capabilities, roadmap

#### Google Developers Blog
- **URL:** https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/
- **Published:** November 19, 2025
- **Focus:** Architecture, agent paradigms, integration patterns

### Antigravity + Claude Code Tutorials

#### Antigravity + Claude Code: Full Integration Guide
- **URL:** https://www.youtube.com/watch?v=yMJcHcCbgi4
- **Duration:** ~35 minutes
- **Focus:** Practical setup, hybrid workflows, MCP tool integration

#### Antigravity + Claude Code: Expert Tips
- **URL:** https://www.youtube.com/watch?v=t3xu9pzfj8Q
- **Duration:** ~8 minutes
- **Focus:** Quick practical examples

#### Antigravity: Complete Beginner to Expert
- **URL:** https://www.youtube.com/watch?v=J04_tSFvBvQ
- **Duration:** ~12 minutes
- **Focus:** Full workflow overview, token optimization

### Expert Implementation Examples

#### Claude Skills Deep Dive (Implementation)
- **URL:** https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
- **Focus:** Technical implementation details, prompt patterns, workflow examples

#### Using Every Claude Code Feature
- **URL:** https://blog.sshh.io/p/how-i-use-every-claude-code-feature
- **Focus:** Advanced Claude Code patterns, task management, delegation

---

## 📊 Quick Reference Tables

### Which Framework to Use?

| Need | Framework | URL |
|------|-----------|-----|
| External service integration | MCP | modelcontextprotocol.io |
| Domain-specific workflows | Agent Skills | platform.claude.com/skills |
| Complete agent system | Agent SDK | platform.claude.com/agent-sdk |
| IDE with agent support | Antigravity | antigravity.google |
| General agent principles | Building Effective Agents | anthropic.com/research |

### Reading Path by Role

**For Architects/Decision Makers:**
1. Building Effective Agents (20 min)
2. MCP Architecture Overview (20 min)
3. Agent Skills Overview (15 min)
4. Total: ~55 minutes

**For Developers Implementing Agents:**
1. Building Agents with Claude Agent SDK (25 min)
2. Claude Agent SDK Workshop Video (100 min)
3. Build an MCP Server (40 min)
4. Agent Skills Technical Docs (20 min)
5. Total: ~185 minutes (comprehensive)

**For Antigravity IDE Users:**
1. Antigravity Blog (10 min)
2. Antigravity + Claude Code Video (35 min)
3. Agent Skills Overview (15 min)
4. Building Effective Agents (20 min)
5. Total: ~80 minutes

---

## 🔐 Security & Best Practices Resources

### Security Guidelines

Covered in:
- Building Agents with Claude Agent SDK (verification section)
- Agent Skills Overview (security considerations)
- Agent SDK Hosting docs (sandboxing requirements)

### Deployment Strategies

**Covered in:**
- Agent SDK Hosting (https://platform.claude.com/docs/en/agent-sdk/hosting)
  - Ephemeral containers
  - Persistent containers
  - Hydrated ephemeral
  - Multi-agent shared

---

## 🎓 Learning Recommendations

### Recommended Study Plan (Comprehensive)

**Week 1: Foundations**
- [ ] Building Effective Agents (1 hour)
- [ ] MCP Architecture Overview (1 hour)
- [ ] Agent SDK Overview (45 min)
- **Total: 2h 45min**

**Week 2: Deep Dive**
- [ ] Claude Agent SDK Workshop Video (100 min)
- [ ] Building Agents with Claude Agent SDK article (30 min)
- [ ] Agent Skills Deep Dive article (20 min)
- **Total: 2h 30min**

**Week 3: Implementation**
- [ ] Build an MCP Server tutorial (40 min, hands-on)
- [ ] Agent Skills Technical Docs (20 min)
- [ ] Antigravity + Claude Code integration videos (50 min)
- **Total: 1h 50min**

**Week 4: Integration & Best Practices**
- [ ] Effective Harnesses for Long-Running Agents (20 min)
- [ ] Agent SDK Hosting guide (20 min)
- [ ] Review frameworks comparison (20 min)
- [ ] Plan your specific implementation (1 hour)
- **Total: 2 hours**

**Grand Total: ~9-10 hours of comprehensive learning**

---

## 📚 Additional Resources

### Community Implementations

**GitHub Collections:**
- Anthropic Skills: https://github.com/anthropics/skills
- MCP Implementations: https://github.com/modelcontextprotocol

### Video Tutorials (YouTube Playlist)

Search for "Claude Agent SDK" or "Antigravity + Claude Code" for latest tutorials.

### API Integration Examples

Requesty Integration with Agent SDK:
- **URL:** https://docs.requesty.ai/integrations/anthropic-agent-sdks

---

## 🎯 Practical Next Steps

1. **Choose Your Use Case**
   - Define what you want to build
   - Identify integration needs
   - Determine deployment model

2. **Select Frameworks**
   - Agents: Claude Agent SDK
   - Integrations: MCP
   - Domain Knowledge: Agent Skills
   - IDE: Antigravity (if coding-focused)

3. **Study Relevant Docs**
   - Use reading path above
   - Focus on your specific use case
   - Review security guidelines

4. **Prototype**
   - Start with simple agent
   - Add one tool at a time
   - Build Skills incrementally
   - Integrate MCP as needed

5. **Deploy**
   - Choose deployment model (ephemeral/persistent/hydrated)
   - Set up sandboxing
   - Configure monitoring
   - Plan rollout

---

## 📞 Support & Community

- **Anthropic Support:** https://support.anthropic.com
- **GitHub Issues:** https://github.com/anthropics/sdk-python/issues
- **Discord Communities:** Search for Claude/Anthropic communities
- **Official Blog:** https://www.anthropic.com/blog

---

**Last Updated:** January 7, 2026  
**Framework Versions Referenced:**
- Claude 3.5 Sonnet (latest)
- Claude Agent SDK (production)
- MCP Specification 2025-06-18
- Agent Skills (December 2025 open standard)

---

This reference guide is designed to be saved locally and updated as new documentation is released.
