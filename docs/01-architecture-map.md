# Architecture Map

這章的目標是建立全局心智模型：四個 `oh-my-*` 專案都在改善 AI coding assistant，但它們選擇的控制點不同。`oh-my-openagent` 把重心放在 runtime；`oh-my-claudecode` 把重心放在 Claude Code 的工作生命週期；`oh-my-codex` 把重心放在 prompt/schema/state 約束；`oh-my-antigravity` 把重心放在共識決策和 session 後學習。

主要依據：

- `graphify-out/GRAPH_REPORT.md`
- `graphify-out/graph.json`
- `graphify-out/FOUR_PROJECTS_DEEP_DIVE.md`
- 四個專案的 `README.md`、`AGENTS.md`、`agents/`、`skills/`、`prompts/`、`tools/`、`hooks/`

## 如何讀 Graphify

graphify 在這個工作區抽出 1047 個節點、51794 條邊、6 個 communities。你可以把它當成「文件與 prompt 的知識地圖」，但不要把每一條 inferred edge 都直接視為作者明示的設計意圖。

讀 graphify 時建議分三層：

| 層級 | 看什麼 | 用途 |
| --- | --- | --- |
| Community | 一群高度相關的文件/角色 | 找出系統模組邊界 |
| God node | 邊數很多的節點 | 找到最值得先讀的核心抽象 |
| Surprising connection | 跨 community 的邊 | 找出跨專案共用概念或設計 lineage |

判讀原則：

- `EXTRACTED` 關係通常來自明確引用或內容抽取，可信度較高。
- `INFERRED` 關係是語意推論，適合當研究線索，仍要回原始檔確認。
- 弱連接節點不一定不重要，有可能只是文件引用少或 graphify 沒抽到足夠上下文。

## 四種架構風格

| 專案 | 架構風格 | 核心問題 | 主要構件 | 先讀入口 |
| --- | --- | --- | --- | --- |
| OMO | Runtime orchestration | 如何讓多個 agent、工具、hook 長時間協作 | `src/agents`、`src/tools`、`src/hooks`、`features/tmux-subagent` | `oh-my-openagent/src/agents/AGENTS.md` |
| OMC | Developer lifecycle OS | 如何把常見開發任務變成可重複的 command/skill 工作流 | `commands`、`skills`、`agents`、`src/tools` | `oh-my-claudecode/docs/ARCHITECTURE.md` |
| OMX | Schema-constrained agent system | 如何用 prompt、schema、state model 限制 agent drift | `prompts`、plugin skills、`src/state`、`src/team` | `oh-my-codex/docs/STATE_MODEL.md` |
| OmA | Consensus and learning extension | 如何用共識 agent 與 session hook 累積本地規則 | `agents`、`skills`、`commands/oma`、`hooks` | `oh-my-antigravity/context/oma-core.md` |

## OMO: Runtime Orchestration

OMO 的核心不是單一 prompt，而是一個可運行的 agent runtime。你可以把它想成一個小型作業系統：agent 是工作角色，tool 是系統呼叫，hook 是事件攔截器，features 是 runtime 能力。

閱讀 OMO 時，先問三個問題：

- 任務如何被路由？看 Atlas、Prometheus、Sisyphus。
- 任務如何被執行？看 `delegate-task`、`call-omo-agent`、`background-task`。
- 任務如何被修正或保護？看 context recovery、rules injector、runtime fallback。

OMO 在 graphify 中主要落在：

- Community 0: Oh My Openagent + Oh My Codex: `oh-my-openagent/packages/omo-codex` / `oh-my-codex/prompts`
- Community 3: Oh My Openagent + Oh My Claudecode: `oh-my-openagent/packages/omo-codex` / `oh-my-openagent/packages/shared-skills`
- Community 4: Oh My Openagent + Oh My Claudecode: `oh-my-openagent/.agents` / `oh-my-openagent/src`

這表示 OMO 在新版 graph 中和 Codex/Claude Code 相容層高度交織，特別是 `omo-codex`、shared skills、runtime source tree 與 prompt surface。

## OMC: Developer Lifecycle OS

OMC 的核心是把 Claude Code 的日常工作變成明確 lifecycle。command 是入口，skill 是流程，agent 是專家角色，tool 是支援性能力。

你可以用這條線理解 OMC：

```text
user intent -> command -> skill workflow -> specialist agent/tool -> verification/release
```

例如 `visual-verdict` 不是單純「看圖片」，而是一個 UI 驗證 workflow；`self-improve` 不是一般 agent，而是把目標、研究、benchmark builder 串成自我改善流程。

OMC 在 graphify 中主要落在：

- Community 1: Oh My Codex + Oh My Claudecode: `oh-my-codex/docs` / `oh-my-codex/skills`
- Community 2: Oh My Claudecode + Oh My Codex: `oh-my-claudecode/skills` / `oh-my-antigravity/commands`
- Community 3: Oh My Openagent + Oh My Claudecode: `oh-my-openagent/packages/omo-codex` / `oh-my-openagent/packages/shared-skills`
- Community 5: Oh My Codex + Oh My Claudecode: `oh-my-codex/docs` / `oh-my-codex/skills`

這表示 OMC 的結構很適合用「任務生命週期」來讀，但新版 graph 也顯示它和 Codex-oriented skill/prompt migration surface 有大量交叉引用。

## OMX: Structured Prompt System

OMX 的核心是把 agent 行為結構化。它大量使用 specialist prompts，但這些 prompt 不只是角色描述，而是搭配 plugin skills、state model、team runtime 形成控制面。

OMX 的閱讀順序應該是：

1. 先讀 `docs/STATE_MODEL.md`，理解狀態和流程約束。
2. 再讀 `prompts/prometheus-strict-*.md`，理解 strict oracle / metis / momus 如何分工。
3. 再讀 plugin skills，例如 `plan`、`team`、`analyze`，看使用者如何進入這些流程。

OMX 在 graphify 中主要落在：

- Community 0: Oh My Openagent + Oh My Codex: `oh-my-openagent/packages/omo-codex` / `oh-my-codex/prompts`
- Community 1: Oh My Codex + Oh My Claudecode: `oh-my-codex/docs` / `oh-my-codex/skills`
- Community 5: Oh My Codex + Oh My Claudecode: `oh-my-codex/docs` / `oh-my-codex/skills`

這表示 OMX 的重點仍在 prompt library、skill entrypoint、docs contract 的組合；新版 graph 也把 OMO 的 Codex compatibility package 拉進同一組語意區域。

## OmA: Consensus and Learning

OmA 的核心是「不要讓單一 agent 直接決策」。它用多個 specialist agent 產生提案，再由 Consensus 合併，由 Director 做最終 gatekeeping，最後透過 learn hook 把 session 中的有效經驗保存成規則。

一個簡化流程是：

```text
task -> specialist proposals -> consensus merge -> director gate -> execute/verify -> learn rules
```

OmA 在 graphify 中主要落在：

- Community 2: Oh My Claudecode + Oh My Codex: `oh-my-claudecode/skills` / `oh-my-antigravity/commands`
- Community 3: Oh My Openagent + Oh My Claudecode: `oh-my-openagent/packages/omo-codex` / `oh-my-openagent/packages/shared-skills`

這表示 OmA 在新版 graph 中主要透過 `commands/oma`、agents 和 skills 和其他專案的 lifecycle / orchestration 概念相連。

## Graphify Community 對照

| Community | 名稱 | 主要對應 | 建議用途 |
| --- | --- | --- | --- |
| 0 | Oh My Openagent + Oh My Codex | `oh-my-openagent/packages/omo-codex`、`oh-my-codex/prompts` | 研究 OMO/OMX compatibility prompt surface |
| 1 | Oh My Codex + Oh My Claudecode | `oh-my-codex/docs`、`oh-my-codex/skills` | 研究 Codex docs contract 和 skill entrypoint |
| 2 | Oh My Claudecode + Oh My Codex | `oh-my-claudecode/skills`、`oh-my-antigravity/commands` | 研究 skill lifecycle 與 OmA command 對照 |
| 3 | Oh My Openagent + Oh My Claudecode | `oh-my-openagent/packages/omo-codex`、`oh-my-openagent/packages/shared-skills` | 研究 shared skill / Codex compatibility layer |
| 4 | Oh My Openagent + Oh My Claudecode | `oh-my-openagent/.agents`、`oh-my-openagent/src` | 研究 OpenAgent runtime source 和 agent guidance |
| 5 | Oh My Codex + Oh My Claudecode | `oh-my-codex/docs`、`oh-my-codex/skills` | 研究 Codex/Claude Code workflow overlap |

## 核心節點怎麼讀

graphify 的 god nodes 不是「最重要功能」的絕對排名，而是「連接最多概念」的文件或抽象。它們適合作為閱讀入口。

| 核心節點 | 讀法 |
| --- | --- |
| `Skill Management CLI` | 觀察 OMC/OMX 如何把 skills 管理成可探索、可調用的能力 |
| `[oh-my-codex] Plan SKILL` | 觀察 OMX 如何把 planning 變成 Codex-oriented workflow |
| `Team Skill` | 比較 OMC/OMX/OmA 的 team 概念差異 |
| `Ralplan` | 追蹤 consensus planning 在不同專案的變體 |
| `oh-my-antigravity (OmA)` | 從 README/context 讀 OmA 的整體設計哲學 |

## 跨專案概念表

| 概念 | OMO | OMC | OMX | OmA |
| --- | --- | --- | --- | --- |
| `plan` | orchestrator 分解任務 | skill/command lifecycle 中的計畫 | strict/state-aware planning skill | consensus 或 oma-plan 流程 |
| `team` | runtime coordination / team mode | coordinated execution skill | Codex team workflow | specialist team + consensus |
| `ralplan` | 被 graphify 連到 OMC skill | consensus planning entrypoint | 部分技能與規劃概念相近 | consensus planning skill |
| `ralph` / loop | 長任務或 persistence 線索 | persistence loop skill | Ralph skill / runtime persistence | loop/recall 類 command |
| `prometheus` | strategic planner agent/prompt | 不是主軸 | strict oracle/metis/momus family | 概念上接近高階規劃，但非主軸 |

## 自測問題

- 如果你只想研究「多 agent runtime」，為什麼應該先讀 OMO 而不是 OMC？
- 為什麼 OMX 的 `prompts/*.md` 不應直接等同於 OMO 的 runtime agent？
- OmA 的 Director 和 OMC/OMX 的 Reviewer 類角色有什麼差異？
- graphify 的 inferred edge 可以怎麼用？什麼情況下不能直接採信？
