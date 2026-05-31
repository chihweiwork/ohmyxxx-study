# ohmyxxx-study: Core Architectural Comparative Analysis & Study Guide

This document is specifically synthesized and formatted for import into **Google NotebookLM**. It provides a comprehensive, high-density reference guide comparing the architectures, prompt designs, safety guardrails, and unique self-evolution loops of the four prominent AI coding tool enhancement frameworks:
1. `oh-my-openagent` (OMO)
2. `oh-my-claudecode` (OMC)
3. `oh-my-codex` (OMX)
4. `oh-my-antigravity` (OmA)

---

## 1. Architectural Comparison Matrix

| Feature | `oh-my-openagent` (OMO) | `oh-my-claudecode` (OMC) | `oh-my-codex` (OMX) | `oh-my-antigravity` (OmA) |
| :--- | :--- | :--- | :--- | :--- |
| **Central Goal** | Multi-Agent Multi-Model Orchestration | Enhanced Developer Tools & Task Lifecycles | Strict Prometheus Oracles & Agent Teams | Autonomous Self-Learning Extension Blocks |
| **Orchestration Model** | Hierarchical Router (Atlas & Prometheus) | Tiered Task Runners with Shared State | strict-oracle Zod-constrained routers | Consensus Planning (Consensus & Director) |
| **Context Optimization** | Compaction Context Injector & Token Limits | Compact session snapshotting (JSON files) | State-Model pruning | Active rule optimization & cache priming |
| **Unique Feature** | Anthropic Limit Auto-Recovery & Tmux agent | `self-improve` autonomous benchmark builder | Strict Oracle guardrails via metis/momus | `/oma:learn` self-evolution post-session hook |
| **Safety / Guardrails** | Run-time fallback handlers | Interactive `visual-verdict` QA loops | Strict JSON schema checks | Consensus review + Director gatekeepers |

---

## 2. Core Project Deep Dives

### 2.1 oh-my-openagent (OMO) — The Multi-Model Orchestrator
*   **Design Paradigm**: Focuses heavily on managing complex, long-running agent workflows across different LLM providers (GPT, Gemini, Opus, Kimi). 
*   **Key Abstractions**:
    *   **Atlas**: A hierarchical orchestrator prompt that acts as a router/coordinator, allocating tasks to specialized agents (e.g., Librarian, Hephaestus, Momus).
    *   **Context Compaction**: Uses the `anthropic-context-window-limit-recovery` hook to detect context bloat, trigger compaction, and inject high-density summaries to preserve long-context reasoning.
    *   **Tmux Subagent Integration**: Provides built-in capabilities to spawn and control multiple terminal panes autonomously for parallel task execution.

### 2.2 oh-my-claudecode (OMC) — The Developer OS & Task Engine
*   **Design Paradigm**: Focuses on enhancing standard Claude Code commands into highly structured developer lifecycles.
*   **Key Abstractions**:
    *   **Command Shims**: Overrides standard commands (`verify`, `release`, `debug`, `ask`) with interactive, visual, and telemetry-aware scripts.
    *   **Self-Improvement Workflow (`self-improve`)**:
        *   `si-goal-clarifier`: Defines structured evaluation benchmarks.
        *   `si-researcher`: Researches the codebase to construct harnesses.
        *   `si-benchmark-builder`: Runs automated benchmark iterations, optimizing its own prompts based on output scores.
    *   **Visual Verdict**: Built-in screenshot and visual-render review loops using headless browsers to verify UI correctness before committing changes.

### 2.3 oh-my-codex (OMX) — The Schema-Constrained Oracle
*   **Design Paradigm**: Employs rigorous structural constraints (Zod, strict JSON schemas) on agent prompt interfaces to eliminate hallucination in complex tool calling.
*   **Key Abstractions**:
    *   **Prometheus Strict Oracle**: A highly disciplined prompt pattern forcing the agent to answer using strict mathematical models and formalized system structures.
    *   **Metis & Momus**: Specialized consultant agents checking proposal correctness (Metis drafts plans, Momus audits and challenges them for edge cases).
    *   **State-Model**: Implements a strict finite state machine (FSM) to manage agent progress, preventing loop behaviors common in autonomous execution.

### 2.4 oh-my-antigravity (OmA) — The Self-Evolving Rule System
*   **Design Paradigm**: Emphasizes dynamic adaptability, local knowledge capture, and consensus-driven execution.
*   **Key Abstractions**:
    *   **`/oma:learn` Hook**:
        *   Runs automatically at the end of a session (`SessionEnd`) when chat history exceeds 10 messages.
        *   Scans the chat log to extract custom debugging tricks, workarounds, or newly discovered codebase paradigms.
        *   Saves these findings as localized rule blocks under `.omg/rules/learned/` so that subsequent sessions instantly gain these capabilities.
    *   **Consensus-Director Loop**: The `consensus` agent collects proposals from specialized personas (Architect, Editor, Reviewer) and compiles them, while the `director` makes the final execution go/no-go decisions.

---

## 3. Knowledge Graph Clustering Insights

Our structural network analysis (Graphify) of **352 document and prompt nodes** across the four repositories identified several critical structural patterns:

*   **God Nodes (Central Hubs)**:
    *   `CLAUDE.md` and `AGENTS.md` across repositories serve as the principal central hubs (high degree centrality). Modifying these files triggers cascading updates throughout the prompt system.
    *   `oh-my-codex/prompts/architect.md` and `oh-my-claudecode/agents/architect.md` show extremely high **Semantic Similarity (cohesion score 0.81)**, confirming direct code lineage and design symmetry shared by the core maintainer.
*   **Sisyphus & Ralph Loops**:
    *   Found in both OMO and OMX. These are long-running state loops designed to keep subagents working on complex tasks asynchronously while preventing terminal execution command timeouts.
*   **Context Optimization Hub**:
    *   A highly clustered community centering around `compaction-context-injector` and `ralph-loop`. This structure proves that as LLMs scale, local context compression becomes the primary bottleneck and engineering focus.

---

## 4. Curated NotebookLM Study Prompts
*Copy and paste these prompts directly into NotebookLM's chat window to generate customized study guides, podcasts, or architecture drafts:*

### 💡 Study Prompt 1: The Self-Evolution Comparison
> "Based on the provided documents, compare how `oh-my-antigravity` learns from previous chat histories (using `/oma:learn`) with how `oh-my-claudecode` uses its `self-improve` benchmark builder. What are the key differences in trigger conditions, data persistence, and how the newly acquired knowledge is injected back into the LLM context?"

### 💡 Study Prompt 2: Design a Hybrid System
> "Act as a Senior AI Software Architect. Design a new, unified 'Ultimate Agentic Enhancer' that combines OMO's multi-model routing (Atlas), OMC's visual verification loop, OMX's strict schema constraints, and OmA's self-learning rule hook. Write a detailed System Prompt and outline the directory structure."

### 💡 Study Prompt 3: Audio Overview Podcast Script
> "Generate a 5-minute host dialogue script (suitable for a tech podcast like NotebookLM's Audio Overview) explaining the concept of 'Context Compaction and Recovery' as implemented in `oh-my-openagent`'s `compaction-context-injector` and how it prevents 429 quota errors."

### 💡 Study Prompt 4: Security and Guardrails Audit
> "Conduct a thorough security and safety comparison of the four projects. Highlight how each project handles dangerous commands (e.g., terminal executions, file overwrites) and how the consensus loop in Antigravity compares with the Prometheus strict oracle schema checks in Codex."
