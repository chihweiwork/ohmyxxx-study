# Graph Report - /home/chihwei/playground/ohmyxxx-study  (2026-05-30)

## Corpus Check
- Large corpus: 4966 files · ~3,937,646 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 352 nodes · 1229 edges · 27 communities detected
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 23 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Skill Management CLI` - 67 edges
2. `[oh-my-codex] Plan SKILL` - 56 edges
3. `oh-my-antigravity (OmA)` - 52 edges
4. `oh-my-codex - Intelligent Multi-Agent Orchestration` - 51 edges
5. `oh-my-antigravity (OmA)` - 48 edges
6. `Team Skill` - 47 edges
7. `oh-my-antigravity (OmA)` - 47 edges
8. `Ralplan (Consensus Planning Alias)` - 46 edges
9. `oh-my-antigravity (OmA)` - 46 edges
10. `oh-my-antigravity (OmA)` - 46 edges

## Surprising Connections (you probably didn't know these)
- `OMC Agents Registry Guide` --semantically_similar_to--> `OMX Core README`  [INFERRED] [semantically similar]
  oh-my-claudecode/src/agents/AGENTS.md → oh-my-codex/README.md
- `OMC Architect Agent` --semantically_similar_to--> `OMX Architect Prompt`  [EXTRACTED] [semantically similar]
  oh-my-claudecode/agents/architect.md → oh-my-codex/prompts/architect.md
- `oh-my-openagent src/agents/AGENTS.md` --references--> `RALPLAN Consensus Planning Entrypoint`  [EXTRACTED]
  oh-my-openagent/src/agents/AGENTS.md → oh-my-claudecode/skills/ralplan/SKILL.md
- `Deep Codebase Initialization Skill` --references--> `oh-my-openagent src/agents/AGENTS.md`  [EXTRACTED]
  oh-my-claudecode/skills/deepinit/SKILL.md → oh-my-openagent/src/agents/AGENTS.md
- `oh-my-openagent src/agents/AGENTS.md` --references--> `Parallel Scientist Orchestration Research Skill`  [EXTRACTED]
  oh-my-openagent/src/agents/AGENTS.md → oh-my-claudecode/skills/sciomc/SKILL.md

## Communities

### Community 0 - "Antigravity CLI Framework"
Cohesion: 0.37
Nodes (59): oh-my-antigravity (OmA), oh-my-antigravity (OmA), oh-my-antigravity (OmA), oh-my-antigravity (OmA), oh-my-antigravity (OmA), [oh-my-antigravity] Architect, [oh-my-antigravity] Blueprint SKILL, [oh-my-antigravity] Consensus (+51 more)

### Community 1 - "OpenCode OpenAgent Orchestration"
Cohesion: 0.07
Nodes (44): Atlas Todo-list Orchestrator Agent, Agent Browser Skill Guide, Anthropic Context Window Limit Recovery Agent Documentation, Atlas Agent Documentation, Background Agent Orchestration Documentation, Boulder Work Plan Tracker Documentation, Built-in Slash Commands Documentation, Built-in Skills Registry Documentation (+36 more)

### Community 2 - "OpenAgent Specialized Personas"
Cohesion: 0.08
Nodes (39): Explore Contextual Grep Agent, Hephaestus Autonomous Deep Worker Agent, Librarian External Search Agent, Metis Pre-planning Consultant Agent, Momus Plan Reviewer Agent, Multimodal-Looker PDF/Image Analysis Agent, Oracle Read-only Consultant Agent, Prometheus Strategic Planner Agent (+31 more)

### Community 3 - "Claude Code Specialized Agents"
Cohesion: 0.08
Nodes (36): OMC Analyst Agent, OMC Architect Agent, OMC Code Reviewer Agent, OMC Code Simplifier Agent, OMC Critic Agent, OMC Debugger Agent, OMC Designer Agent, OMC Document Specialist Agent (+28 more)

### Community 4 - "Codex Specialized Prompts"
Cohesion: 0.14
Nodes (35): AI Slop Cleaner Skill, Analyst, Autoresearch Skill, Best-Practice Research, Build Fixer, Code Review Skill, Code Reviewer, Code Simplifier (+27 more)

### Community 5 - "Claude Code Compatibility Commands"
Cohesion: 0.07
Nodes (30): oh-my-claudecode AGENTS.md, oh-my-claudecode CLAUDE.md, OMC ask compatibility command, OMC autoresearch compatibility command, OMC ccg compatibility command, OMC configure-notifications compatibility command, OMC debug compatibility command, OMC deep-dive compatibility command (+22 more)

### Community 6 - "OpenCode Hooks and Tools"
Cohesion: 0.09
Nodes (29): oh-my-openagent/src/hooks/auto-update-checker/AGENTS.md, oh-my-openagent/src/tools/background-task/AGENTS.md, oh-my-openagent/src/tools/call-omo-agent/AGENTS.md, oh-my-openagent/src/tools/delegate-task/AGENTS.md, oh-my-openagent/docs/AGENTS.md, oh-my-openagent/src/tools/hashline-edit/AGENTS.md, oh-my-openagent/src/hooks/AGENTS.md, oh-my-openagent/src/hooks/keyword-detector/AGENTS.md (+21 more)

### Community 7 - "Codex Local Advisor Skills"
Cohesion: 0.24
Nodes (20): Analyze — Read-Only Deep Analysis, Ask Claude compatibility shim, Ask Gemini compatibility shim, Ask (Local Advisor CLI), Build Fix deprecated, Configure OMX Notifications, Deepsearch deprecated, Design Skill (+12 more)

### Community 8 - "Claude Code Core Skills & Design"
Cohesion: 0.13
Nodes (19): Claude Code Goal Adapter Design, Architecture Guide, Orchestration Instructions (CLAUDE.md), Ask Skill, Cancel Skill, Deep Dive Skill, External Context Skill, OMC Doctor Skill (+11 more)

### Community 9 - "Claude Code Self-Improvement Workflow"
Cohesion: 0.39
Nodes (8): Self-Improvement Data Contracts, Self-Improvement Benchmark Builder, Self-Improvement Goal Clarifier, Self-Improvement Researcher, Self-Improvement Orchestrator Skill, Self-Improvement Goal Template, Self-Improvement Harness Template, Self-Improvement Experiment Idea Template

### Community 10 - "Agent Autoresearch Showcase & Missions"
Cohesion: 0.8
Nodes (6): [oh-my-antigravity] Research SKILL, Autoresearch Goal, Autoresearch, Best-Practice Research, Autoresearch pilot missions, Autoresearch Research Showcase

### Community 11 - "OpenCode Atlas Multi-Model Prompts"
Cohesion: 0.4
Nodes (5): oh-my-openagent/packages/prompts-core/prompts/atlas/default.md, oh-my-openagent/packages/prompts-core/prompts/atlas/gemini.md, oh-my-openagent/packages/prompts-core/prompts/atlas/gpt.md, oh-my-openagent/packages/prompts-core/prompts/atlas/kimi.md, oh-my-openagent/packages/prompts-core/prompts/atlas/opus-4-7.md

### Community 12 - "Claude Code Agent Templates & Matrix"
Cohesion: 0.67
Nodes (4): Agent Prompt Templates Guide, Model Compatibility Matrix, Tiered Agents v2 Design, Docs Agents Guide

### Community 13 - "OpenCode Prometheus Prompts"
Cohesion: 0.67
Nodes (3): oh-my-openagent/packages/prompts-core/prompts/prometheus/default.md, oh-my-openagent/packages/prompts-core/prompts/prometheus/gemini.md, oh-my-openagent/packages/prompts-core/prompts/prometheus/gpt.md

### Community 14 - "Claude Code Benchmarks"
Cohesion: 1.0
Nodes (2): Benchmark Suite Guide, Benchmark Results Guide

### Community 15 - "Claude Code Seminar Showcases"
Cohesion: 1.0
Nodes (2): Seminar Demos Guide, Seminar Screenshots Guide

### Community 16 - "Codex Wiki System"
Cohesion: 1.0
Nodes (1): Wiki

### Community 17 - "Claude-Codex-Gemini Interoperability"
Cohesion: 1.0
Nodes (1): Claude-Codex-Gemini Orchestration Skill

### Community 18 - "Codex Wiki Skill"
Cohesion: 1.0
Nodes (1): Persistent LLM Wiki Skill

### Community 19 - "Evidence-Driven Tracing"
Cohesion: 1.0
Nodes (1): Evidence-Driven Tracing Skill

### Community 20 - "Claude Code Notifications"
Cohesion: 1.0
Nodes (1): Configure Notifications Skill

### Community 21 - "Claude Code Memory"
Cohesion: 1.0
Nodes (1): Remember Skill

### Community 22 - "Claude Code Diagnostics"
Cohesion: 1.0
Nodes (1): Debug Skill

### Community 23 - "Claude Code Rules Engine"
Cohesion: 1.0
Nodes (1): Rules Templates Guide

### Community 24 - "Claude Code Vendor MCP Contract"
Cohesion: 1.0
Nodes (1): OMC Vendor MCP Server README

### Community 25 - "Codex Explore Prompt"
Cohesion: 1.0
Nodes (1): OMX Explore Lightweight Instructions

### Community 26 - "Codex SparkShell Prompt"
Cohesion: 1.0
Nodes (1): OMX SparkShell Lightweight Instructions

## Knowledge Gaps
- **128 isolated node(s):** `oh-my-openagent/README.md`, `oh-my-openagent/script/AGENTS.md`, `oh-my-openagent/packages/prompts-core/prompts/atlas/gpt.md`, `oh-my-openagent/packages/prompts-core/prompts/atlas/gemini.md`, `oh-my-openagent/packages/prompts-core/prompts/atlas/opus-4-7.md` (+123 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Claude Code Benchmarks`** (2 nodes): `Benchmark Suite Guide`, `Benchmark Results Guide`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Claude Code Seminar Showcases`** (2 nodes): `Seminar Demos Guide`, `Seminar Screenshots Guide`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Codex Wiki System`** (1 nodes): `Wiki`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Claude-Codex-Gemini Interoperability`** (1 nodes): `Claude-Codex-Gemini Orchestration Skill`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Codex Wiki Skill`** (1 nodes): `Persistent LLM Wiki Skill`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Evidence-Driven Tracing`** (1 nodes): `Evidence-Driven Tracing Skill`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Claude Code Notifications`** (1 nodes): `Configure Notifications Skill`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Claude Code Memory`** (1 nodes): `Remember Skill`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Claude Code Diagnostics`** (1 nodes): `Debug Skill`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Claude Code Rules Engine`** (1 nodes): `Rules Templates Guide`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Claude Code Vendor MCP Contract`** (1 nodes): `OMC Vendor MCP Server README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Codex Explore Prompt`** (1 nodes): `OMX Explore Lightweight Instructions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Codex SparkShell Prompt`** (1 nodes): `OMX SparkShell Lightweight Instructions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `oh-my-openagent src/agents/AGENTS.md` connect `OpenAgent Specialized Personas` to `OpenCode OpenAgent Orchestration`, `Codex Specialized Prompts`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `Atlas Todo-list Orchestrator Agent` connect `OpenCode OpenAgent Orchestration` to `OpenAgent Specialized Personas`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **What connects `oh-my-openagent/README.md`, `oh-my-openagent/script/AGENTS.md`, `oh-my-openagent/packages/prompts-core/prompts/atlas/gpt.md` to the rest of the system?**
  _128 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `OpenCode OpenAgent Orchestration` be split into smaller, more focused modules?**
  _Cohesion score 0.07 - nodes in this community are weakly interconnected._
- **Should `OpenAgent Specialized Personas` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Claude Code Specialized Agents` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Codex Specialized Prompts` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._