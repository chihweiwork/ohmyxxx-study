# Agent Skill Tool Map

這份索引用來回答：「這些 agent、skill、tool、command、hook、prompt 到底各自負責什麼？」它不是完整百科，而是學習架構時的核心地圖。完整節點請看 `graphify-out/graph.json`。

## 分類規則

不同專案對同一個詞的用法不完全一致，因此本文件用功能而不是檔名做分類。

| 類別 | 判斷方式 | 常見形式 |
| --- | --- | --- |
| Agent | 扮演決策、執行、審核、研究等角色 | `agents/*.md`、`src/agents/*/AGENTS.md` |
| Prompt | specialist instruction，但不一定是 runtime process | `prompts/*.md` |
| Skill | 可重用工作流或能力入口 | `skills/*/SKILL.md`、plugin skills |
| Tool | 有實作的可調用能力，通常處理 I/O 或 runtime action | `src/tools/*` |
| Hook | 在事件前後插入控制、注入、修復、驗證 | `src/hooks/*`、`hooks/scripts/*` |
| Command | 使用者可直接觸發的入口 | `commands/*.md`、`commands/oma/*.toml` |

## 角色分類

先用角色理解，比背名稱更有效：

| 角色 | 代表項目 | 責任 |
| --- | --- | --- |
| Planner | Prometheus、Planner、Metis、Ralplan | 拆解任務、提出計畫 |
| Executor | Hephaestus、Executor、Team Executor、Editor | 實作或執行工作 |
| Reviewer | Momus、Reviewer、Code Reviewer、Security Reviewer | 挑錯、驗證、審核 |
| Researcher | Librarian、Researcher、Scientist、Autoresearch | 搜尋、研究、實驗 |
| Orchestrator | Atlas、Sisyphus、Team Orchestrator、Consensus | 協調多角色或多步驟 |
| Gatekeeper | Director、strict oracle/state model、verify hooks | 決定能否進入下一步 |
| Memory/Context | context injector、Ralph、Wiki、Learn | 保存或壓縮上下文 |

## oh-my-openagent (OMO)

OMO 的項目最接近 runtime 元件。Agent 會透過 tool 執行，hook 會干預 runtime 行為。

| 類別 | 項目 | 來源 | 用途 | 優先級 |
| --- | --- | --- | --- | --- |
| Agent | Atlas | `oh-my-openagent/src/agents/atlas/AGENTS.md` | todo-list orchestrator，負責路由與協調 | 核心 |
| Agent | Prometheus | `oh-my-openagent/src/agents/prometheus/AGENTS.md` | strategic planner，負責高階計畫 | 核心 |
| Agent | Sisyphus | `oh-my-openagent/src/agents/sisyphus/AGENTS.md` | main long-running orchestrator | 核心 |
| Agent | Sisyphus-Junior | `oh-my-openagent/src/agents/sisyphus-junior/AGENTS.md` | category-spawned executor | 進階 |
| Agent | Hephaestus | `oh-my-openagent/src/agents/hephaestus/AGENTS.md` | autonomous deep worker，偏長任務執行 | 核心 |
| Agent | Oracle | `oh-my-openagent/src/agents/AGENTS.md` | read-only consultant，適合諮詢與審視 | 常用 |
| Agent | Librarian | `oh-my-openagent/src/agents/AGENTS.md` | external search specialist | 常用 |
| Agent | Explore | `oh-my-openagent/src/agents/AGENTS.md` | contextual grep / codebase exploration | 常用 |
| Agent | Multimodal-Looker | `oh-my-openagent/src/agents/AGENTS.md` | PDF/image analysis | 進階 |
| Agent | Metis | `oh-my-openagent/src/agents/AGENTS.md` | pre-planning consultant | 核心 |
| Agent | Momus | `oh-my-openagent/src/agents/AGENTS.md` | plan reviewer | 核心 |
| Tool | `call-omo-agent` | `oh-my-openagent/src/tools/call-omo-agent` | 呼叫 OMO subagent | 核心 |
| Tool | `delegate-task` | `oh-my-openagent/src/tools/delegate-task` | 任務委派、模型選擇、subagent resolution | 核心 |
| Tool | `background-task` | `oh-my-openagent/src/tools/background-task` | 長任務背景執行與狀態查詢 | 核心 |
| Tool | `hashline-edit` | `oh-my-openagent/src/tools/hashline-edit` | hashline-based safe editing | 常用 |
| Tool | `look-at` | `oh-my-openagent/src/tools/look-at` | 多模態查看檔案/圖片 | 常用 |
| Tool | `skill` / `skill-mcp` | `oh-my-openagent/src/tools/skill` | skill discovery/loading | 常用 |
| Hook | context recovery | `oh-my-openagent/src/hooks/anthropic-context-window-limit-recovery` | context window limit recovery | 核心 |
| Hook | compaction injector | `oh-my-openagent/src/hooks/compaction-context-injector` | 注入壓縮後上下文 | 核心 |
| Hook | rules injector | `oh-my-openagent/src/hooks/rules-injector` | 注入規則 | 常用 |
| Hook | runtime fallback | `oh-my-openagent/src/hooks/runtime-fallback` | runtime fallback handling | 常用 |

OMO 查表方式：

- 研究任務分派：看 Atlas、Prometheus、Sisyphus、`delegate-task`。
- 研究長任務：看 Hephaestus、Sisyphus、`background-task`。
- 研究穩定性：看 context recovery、compaction injector、runtime fallback。

Atlas / Prometheus prompt variants 不是新的 agent，而是同一 agent 針對不同模型家族的 prompt family：

| Agent | Variant | 來源 | 用途 |
| --- | --- | --- | --- |
| Atlas | default | `oh-my-openagent/packages/prompts-core/prompts/atlas/default.md` | 通用 Atlas orchestration prompt |
| Atlas | gpt | `oh-my-openagent/packages/prompts-core/prompts/atlas/gpt.md` | GPT 模型專用 Atlas prompt calibration |
| Atlas | gemini | `oh-my-openagent/packages/prompts-core/prompts/atlas/gemini.md` | Gemini 模型專用 Atlas prompt calibration |
| Prometheus | default | `oh-my-openagent/packages/prompts-core/prompts/prometheus/default.md` | 通用 Prometheus planning prompt |
| Prometheus | gpt | `oh-my-openagent/packages/prompts-core/prompts/prometheus/gpt.md` | GPT 模型專用 Prometheus prompt calibration |
| Prometheus | gemini | `oh-my-openagent/packages/prompts-core/prompts/prometheus/gemini.md` | Gemini 模型專用 Prometheus prompt calibration |

## oh-my-claudecode (OMC)

OMC 的項目應該按 workflow 讀。Command 是使用者入口，skill 定義流程，agent 提供 specialist 判斷，tool 支援資料與狀態操作。

| 類別 | 項目 | 來源 | 用途 | 優先級 |
| --- | --- | --- | --- | --- |
| Agent | Architect | `oh-my-claudecode/agents/architect.md` | architecture design | 核心 |
| Agent | Planner | `oh-my-claudecode/agents/planner.md` | plan drafting | 核心 |
| Agent | Executor | `oh-my-claudecode/agents/executor.md` | implementation execution | 核心 |
| Agent | Verifier | `oh-my-claudecode/agents/verifier.md` | verification | 核心 |
| Agent | Code Reviewer | `oh-my-claudecode/agents/code-reviewer.md` | code review | 常用 |
| Agent | Debugger | `oh-my-claudecode/agents/debugger.md` | debugging | 常用 |
| Agent | Scientist | `oh-my-claudecode/agents/scientist.md` | experiment/research | 進階 |
| Agent | Tracer | `oh-my-claudecode/agents/tracer.md` | evidence-driven tracing | 常用 |
| Skill | Plan | `oh-my-claudecode/skills/plan/SKILL.md` | strategic planning | 核心 |
| Skill | Self Improve | `oh-my-claudecode/skills/self-improve/SKILL.md` | prompt/workflow benchmark loop | 核心 |
| Skill | Autoresearch | `oh-my-claudecode/skills/autoresearch/SKILL.md` | automated research | 常用 |
| Skill | SciOMC | `oh-my-claudecode/skills/sciomc/SKILL.md` | parallel scientist orchestration | 進階 |
| Skill | Visual Verdict | `oh-my-claudecode/skills/visual-verdict/SKILL.md` | screenshot-based UI QA | 常用 |
| Skill | RALPLAN | `oh-my-claudecode/skills/ralplan/SKILL.md` | consensus planning entrypoint | 核心 |
| Skill | Team | `oh-my-claudecode/skills/team/SKILL.md` | coordinated execution | 核心 |
| Skill | Ralph | `oh-my-claudecode/skills/ralph/SKILL.md` | persistence loop | 進階 |
| Tool | memory/wiki/state tools | `oh-my-claudecode/src/tools` | 本地記憶、wiki、state 操作 | 常用 |
| Tool | LSP/diagnostics tools | `oh-my-claudecode/src/tools` | code intelligence and diagnostics | 常用 |

OMC 查表方式：

- 想了解「開發流程」：從 `commands/` 追到 skills。
- 想了解「專家角色」：看 `agents/*.md`。
- 想了解「狀態和記憶」：看 `src/tools` 的 memory/wiki/state 類工具。

## oh-my-codex (OMX)

OMX 的 prompt 和 skill 要一起讀。Prompt 定義 specialist 行為，plugin skill 定義入口與流程，state/runtime module 定義約束與執行環境。

| 類別 | 項目 | 來源 | 用途 | 優先級 |
| --- | --- | --- | --- | --- |
| Prompt | Prometheus Strict Oracle | `oh-my-codex/prompts/prometheus-strict-oracle.md` | strict oracle prompt | 核心 |
| Prompt | Prometheus Strict Metis | `oh-my-codex/prompts/prometheus-strict-metis.md` | strict planner/consultant | 核心 |
| Prompt | Prometheus Strict Momus | `oh-my-codex/prompts/prometheus-strict-momus.md` | strict reviewer/auditor | 核心 |
| Prompt | Architect | `oh-my-codex/prompts/architect.md` | architecture specialist | 核心 |
| Prompt | Team Orchestrator | `oh-my-codex/prompts/team-orchestrator.md` | team coordination | 核心 |
| Prompt | Executor | `oh-my-codex/prompts/executor.md` | execution specialist | 核心 |
| Prompt | Planner | `oh-my-codex/prompts/planner.md` | planning specialist | 核心 |
| Prompt | Security Reviewer | `oh-my-codex/prompts/security-reviewer.md` | security review | 常用 |
| Prompt | Quality Reviewer | `oh-my-codex/prompts/quality-reviewer.md` | quality review | 常用 |
| Prompt | Code Simplifier | `oh-my-codex/prompts/code-simplifier.md` | simplification/refactor review | 常用 |
| Skill | Prometheus Strict | `oh-my-codex/plugins/oh-my-codex/skills/prometheus-strict/SKILL.md` | strict workflow entry | 核心 |
| Skill | Plan | `oh-my-codex/plugins/oh-my-codex/skills/plan/SKILL.md` | Codex planning workflow | 核心 |
| Skill | Team | `oh-my-codex/plugins/oh-my-codex/skills/team/SKILL.md` | team workflow | 核心 |
| Skill | Analyze | `oh-my-codex/plugins/oh-my-codex/skills/analyze/SKILL.md` | read-only deep analysis | 常用 |
| Skill | Ralph | `oh-my-codex/plugins/oh-my-codex/skills/ralph/SKILL.md` | persistence loop | 進階 |
| Skill | Pipeline | `oh-my-codex/plugins/oh-my-codex/skills/pipeline/SKILL.md` | staged workflow | 進階 |
| Runtime | subagents/team/hooks | `oh-my-codex/src` | runtime support modules | 進階 |

OMX 查表方式：

- 想了解嚴格約束：看 Prometheus Strict family 和 `STATE_MODEL.md`。
- 想了解日常入口：看 `plan`、`team`、`analyze` skills。
- 想比較 OMC：對照 OMC agents 與 OMX prompts 的同名角色。

## oh-my-antigravity (OmA)

OmA 的項目應按決策流程讀：specialist 提案、Consensus 合成、Director gate、Executor/Verifier 完成工作、Learn 保存經驗。

| 類別 | 項目 | 來源 | 用途 | 優先級 |
| --- | --- | --- | --- | --- |
| Agent | Director | `oh-my-antigravity/agents/director.md` | final gatekeeper | 核心 |
| Agent | Consensus | `oh-my-antigravity/agents/consensus.md` | merge specialist proposals | 核心 |
| Agent | Architect | `oh-my-antigravity/agents/architect.md` | architecture proposal | 核心 |
| Agent | Reviewer | `oh-my-antigravity/agents/reviewer.md` | review and critique | 核心 |
| Agent | Researcher | `oh-my-antigravity/agents/researcher.md` | research | 常用 |
| Agent | Editor | `oh-my-antigravity/agents/editor.md` | editing implementation | 常用 |
| Agent | Executor | `oh-my-antigravity/agents/executor.md` | execution | 核心 |
| Agent | Verifier | `oh-my-antigravity/agents/verifier.md` | verification | 核心 |
| Skill | Learn | `oh-my-antigravity/skills/learn/SKILL.md` | session learning and rule capture | 核心 |
| Skill | Ralplan | `oh-my-antigravity/skills/ralplan/SKILL.md` | consensus planning | 核心 |
| Skill | Plan | `oh-my-antigravity/skills/plan/SKILL.md` | planning | 核心 |
| Skill | Execute | `oh-my-antigravity/skills/execute/SKILL.md` | execution workflow | 核心 |
| Skill | Context Optimize | `oh-my-antigravity/skills/context-optimize/SKILL.md` | context optimization | 常用 |
| Command | `oma team-*` | `oh-my-antigravity/commands/oma` | team planning/execution/verification | 核心 |
| Command | `oma consensus` | `oh-my-antigravity/commands/oma/consensus.toml` | consensus workflow | 核心 |
| Hook | learn hook | `oh-my-antigravity/hooks/scripts/learn.js` | session-end learning | 核心 |

OmA 查表方式：

- 想了解共識決策：看 Consensus、Director、Ralplan。
- 想了解執行閉環：看 Execute、Executor、Verifier、team commands。
- 想了解學習機制：看 Learn skill 和 learn hook script。

## 如何使用這份索引

- 要理解「誰負責決策」：看 Atlas、Prometheus、Planner、Director、Consensus。
- 要理解「誰負責執行」：看 Hephaestus、Executor、Team Executor、Editor。
- 要理解「誰負責審核」：看 Momus、Verifier、Reviewer、Code Reviewer、Security Reviewer。
- 要理解「怎麼避免失控」：看 OMO hooks、OMC verify/visual-verdict、OMX strict prompts/state model、OmA Director gatekeeping。
- 要理解「怎麼保存上下文」：看 OMO compaction、OMC memory/wiki/state tools、OMX Ralph/wiki/state、OmA learn hook。

## 自測問題

- 為什麼 `skill` 不等於 `tool`？
- 哪些項目是 planner？哪些項目是 gatekeeper？
- OMO 的 hook 和 OmA 的 hook 解決的是同一類問題嗎？
- 如果要設計一個新的 UI 驗證流程，你會優先借鑑 OMC 哪些項目？
