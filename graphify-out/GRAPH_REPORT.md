# Graph Report - /home/chihwei/playground/ohmyxxx-study  (2026-06-07)

## Corpus Check
- Large corpus: 5916 files · ~4,545,359 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 1047 nodes · 51794 edges · 6 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `src/cli/run/ — Non-Interactive Session Launcher` - 668 edges
2. `Prometheus - Strategic Planning Consultant` - 568 edges
3. `Ultrawork Notepad — <one-line goal>` - 549 edges
4. `[oh-my-openagent] Default` - 529 edges
5. `Reference Documentation` - 505 edges
6. `[oh-my-openagent] Default` - 494 edges
7. `src/config/ — Zod v4 Schema System` - 482 edges
8. `oh-my-claudecode - Intelligent Multi-Agent Orchestration` - 477 edges
9. `src/ — Plugin Source` - 473 edges
10. `src` - 466 edges

## Surprising Connections (you probably didn't know these)
- `oh-my-antigravity (OmA)` --semantically_similar_to--> `Orchestration System Guide`  [EXTRACTED] [semantically similar]
  oh-my-antigravity/README.md → oh-my-openagent/docs/guide/orchestration.md
- `Prompt Migration Changelog` --semantically_similar_to--> `[oh-my-antigravity] Architect`  [EXTRACTED] [semantically similar]
  oh-my-codex/docs/prompt-migration-changelog.md → oh-my-antigravity/agents/architect.md
- `Prompt Migration Changelog` --semantically_similar_to--> `[oh-my-antigravity] Debugger`  [EXTRACTED] [semantically similar]
  oh-my-codex/docs/prompt-migration-changelog.md → oh-my-antigravity/agents/debugger.md
- `Prompt Migration Changelog` --semantically_similar_to--> `[oh-my-antigravity] Executor`  [EXTRACTED] [semantically similar]
  oh-my-codex/docs/prompt-migration-changelog.md → oh-my-antigravity/agents/executor.md
- `Prompt Migration Changelog` --semantically_similar_to--> `[oh-my-antigravity] Product`  [EXTRACTED] [semantically similar]
  oh-my-codex/docs/prompt-migration-changelog.md → oh-my-antigravity/agents/product.md

## Communities

### Community 0 - "Oh My Openagent + Oh My Codex: oh my openagent/packages/omo codex / oh my codex/prompts"
Cohesion: 0.17
Nodes (241): [oh-my-antigravity] Consultant, [oh-my-antigravity] Planner, [oh-my-antigravity] Quick, [oh-my-antigravity] Reviewer, [oh-my-antigravity] Approval, [oh-my-antigravity] Goal, [oh-my-antigravity] Hooks Test, [oh-my-antigravity] Loop (+233 more)

### Community 1 - "Oh My Codex + Oh My Claudecode: oh my codex/docs / oh my codex/skills"
Cohesion: 0.19
Nodes (230): [oh-my-antigravity] Interview, [oh-my-antigravity] Doctor, [oh-my-antigravity] Hud, [oh-my-antigravity] Interview, [oh-my-antigravity] Launch, [oh-my-antigravity] Notify, [oh-my-antigravity] Status, [oh-my-antigravity] Team (+222 more)

### Community 2 - "Oh My Claudecode + Oh My Codex: oh my claudecode/skills / oh my antigravity/commands"
Cohesion: 0.24
Nodes (195): [oh-my-antigravity] Architect, [oh-my-antigravity] Consensus, [oh-my-antigravity] Director, [oh-my-antigravity] Editor, [oh-my-antigravity] Executor, [oh-my-antigravity] Product, [oh-my-antigravity] Researcher, [oh-my-antigravity] Verifier (+187 more)

### Community 3 - "Oh My Openagent + Oh My Claudecode: oh my openagent/packages/omo codex / oh my openagent/packages/shared skills"
Cohesion: 0.2
Nodes (187): [oh-my-antigravity] Debugger, [oh-my-antigravity] Cache, [oh-my-antigravity] Memory, [oh-my-claudecode] Code Simplifier, [oh-my-claudecode] Debugger, SWE-bench Benchmark Suite, SWE-bench Verified Results, OMC debug (+179 more)

### Community 4 - "Oh My Openagent + Oh My Claudecode: oh my openagent/.agents / oh my openagent/src"
Cohesion: 0.19
Nodes (166): [oh-my-antigravity] Hooks, oh-my-antigravity Extension Installation Guide, [oh-my-claudecode] Build Fixer, OMC skill, Developer API Reference, Hooks System, Local Plugin Installation, Features Reference (v3.1 - v3.4) (+158 more)

### Community 5 - "Oh My Codex + Oh My Claudecode: oh my codex/docs / oh my codex/skills"
Cohesion: 0.57
Nodes (28): [oh-my-antigravity] Stop, OMC ask, OpenClaw / Clawhip Routing Contract, Ask, Runtime command / event / snapshot schema, OpenClaw-Integrationsleitfaden (lokalisierte Prompt-Optimierung), Guía de integración de OpenClaw (ajuste de prompts localizado), Guide d’intégration OpenClaw (réglage localisé des prompts) (+20 more)

## Knowledge Gaps
- **5 isolated node(s):** `[oh-my-codex] Verifier Investigation`, `OMX SparkShell Lightweight Instructions`, `[oh-my-openagent] PullRequestTemplate`, `[oh-my-openagent] Windows Git Bash`, `Auth service feature brief`
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `src/cli/run/ — Non-Interactive Session Launcher` connect `Oh My Openagent + Oh My Claudecode: oh my openagent/packages/omo codex / oh my openagent/packages/shared skills` to `Oh My Openagent + Oh My Codex: oh my openagent/packages/omo codex / oh my codex/prompts`, `Oh My Codex + Oh My Claudecode: oh my codex/docs / oh my codex/skills`, `Oh My Claudecode + Oh My Codex: oh my claudecode/skills / oh my antigravity/commands`, `Oh My Openagent + Oh My Claudecode: oh my openagent/.agents / oh my openagent/src`, `Oh My Codex + Oh My Claudecode: oh my codex/docs / oh my codex/skills`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `src/config/ — Zod v4 Schema System` connect `Oh My Openagent + Oh My Claudecode: oh my openagent/.agents / oh my openagent/src` to `Oh My Openagent + Oh My Codex: oh my openagent/packages/omo codex / oh my codex/prompts`, `Oh My Codex + Oh My Claudecode: oh my codex/docs / oh my codex/skills`, `Oh My Claudecode + Oh My Codex: oh my claudecode/skills / oh my antigravity/commands`, `Oh My Openagent + Oh My Claudecode: oh my openagent/packages/omo codex / oh my openagent/packages/shared skills`, `Oh My Codex + Oh My Claudecode: oh my codex/docs / oh my codex/skills`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `Prometheus - Strategic Planning Consultant` connect `Oh My Openagent + Oh My Claudecode: oh my openagent/packages/omo codex / oh my openagent/packages/shared skills` to `Oh My Openagent + Oh My Codex: oh my openagent/packages/omo codex / oh my codex/prompts`, `Oh My Codex + Oh My Claudecode: oh my codex/docs / oh my codex/skills`, `Oh My Claudecode + Oh My Codex: oh my claudecode/skills / oh my antigravity/commands`, `Oh My Openagent + Oh My Claudecode: oh my openagent/.agents / oh my openagent/src`, `Oh My Codex + Oh My Claudecode: oh my codex/docs / oh my codex/skills`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **What connects `[oh-my-codex] Verifier Investigation`, `OMX SparkShell Lightweight Instructions`, `[oh-my-openagent] PullRequestTemplate` to the rest of the system?**
  _5 weakly-connected nodes found - possible documentation gaps or missing edges._