# Project Guides

本章逐一說明四個專案該怎麼讀。目標是讓你讀原始碼與文件時知道「先抓哪條主線」，而不是在上千個 Markdown、TypeScript、TOML 檔案中迷路。

建議每個專案都用同一個問題框架閱讀：

- 它把使用者意圖放在哪個入口？
- 它如何規劃、委派、執行、驗證？
- 它如何避免 agent drift、上下文爆炸或錯誤決策？
- 它的 agent / skill / tool / hook / prompt 哪些是核心，哪些只是支援？

## oh-my-openagent (OMO)

OMO 最像完整的 agent runtime。它不只提供 prompt 或 skill，而是有 agent registry、tool implementation、hook pipeline、tmux/background execution 和多模型 prompt variants。

### 心智模型

把 OMO 想成一個「agent runtime shell」：

```text
user task
  -> orchestrator agent
  -> specialist agent
  -> tool execution
  -> hook correction/recovery
  -> background/session continuation
```

這個模型的重點是 runtime 能力。OMO 關心的不只是「agent 應該怎麼想」，還包含「agent 如何被建立、如何呼叫別的 agent、如何在背景跑、如何從 context 或 runtime error 中恢復」。

### 核心流程

1. 使用者任務進入 Atlas、Prometheus、Sisyphus 或其他 orchestrator。
2. Orchestrator 依任務類型選擇 specialist agent，例如 Hephaestus、Librarian、Oracle、Metis、Momus。
3. Agent 透過 `delegate-task`、`call-omo-agent`、`background-task` 等工具展開同步或背景任務。
4. Hooks 在前後攔截與修正，例如 context recovery、rules injection、fallback、team gating。
5. 如果任務很長，背景任務、tmux subagent、session recovery 會讓工作延續。

### 先讀

- `oh-my-openagent/src/agents/AGENTS.md`
- `oh-my-openagent/src/tools/AGENTS.md`
- `oh-my-openagent/src/hooks/AGENTS.md`
- `oh-my-openagent/packages/prompts-core/prompts/atlas/default.md`
- `oh-my-openagent/packages/prompts-core/prompts/prometheus/default.md`

### 讀檔提示

- 看到 `AGENTS.md`，先判斷它是在描述目錄規則、agent persona，還是 runtime 文件。
- 看到 `tools.ts` 或 `index.ts`，通常代表真實工具實作，不只是 prompt instruction。
- 看到 `hooks/`，要問它是「安全限制」、「上下文注入」、「錯誤恢復」還是「使用者體驗修正」。

### 容易誤解

- OMO 的 agent 不是單純 Markdown 角色。很多 agent 會被 runtime tool 和 hook 包起來。
- OMO 的 hooks 很多，不代表每個都同等重要。先看 context recovery、compaction、rules injector、fallback。
- Atlas 和 Prometheus 都像 planner，但 Atlas 偏 orchestrator/router，Prometheus 偏 strategy/planning。

### 學完應能回答

- `delegate-task` 和 `call-omo-agent` 的差異是什麼？
- OMO 為什麼需要 background task？
- OMO 的 context recovery 解決了哪類失敗？

## oh-my-claudecode (OMC)

OMC 是 Claude Code 的 developer OS。它把常見開發任務包成 commands，再把可重用流程放進 skills，並用 agents 作為 specialist persona。

### 心智模型

把 OMC 想成「開發生命週期套件」：

```text
command
  -> skill workflow
  -> specialist agent/tool
  -> artifact
  -> verification or release
```

它的核心價值是把日常工程活動制度化，例如 research、plan、debug、verify、release、visual QA、self-improve。

### 核心流程

1. 使用者呼叫 command，例如 `debug`、`verify`、`visual-verdict`、`self-improve`。
2. Command 對應到 skill 或 CLI implementation。
3. Skill 指定工作流程、輸入資料、產物和驗證方式。
4. 遇到需要專家判斷時，使用 `agents/*.md` 的 specialist role。
5. 透過 tools 處理 memory、wiki、state、LSP、diagnostics 等支援能力。

### 先讀

- `oh-my-claudecode/README.md`
- `oh-my-claudecode/docs/ARCHITECTURE.md`
- `oh-my-claudecode/docs/TOOLS.md`
- `oh-my-claudecode/commands/`
- `oh-my-claudecode/skills/plan/SKILL.md`
- `oh-my-claudecode/skills/self-improve/SKILL.md`
- `oh-my-claudecode/agents/`

### 讀檔提示

- 先從 `commands/*.md` 找入口，再追到對應 skill。
- 讀 skill 時要找：觸發條件、輸入、步驟、產物、驗證。
- 讀 agent 時要找：它是 planner、executor、reviewer、researcher 還是 verifier。

### 容易誤解

- OMC 的 command 不是只有 alias。很多 command 代表一整段工作流。
- `self-improve` 不是一般「自我反省」prompt，而是包含 goal clarifier、researcher、benchmark builder 的工作鏈。
- `visual-verdict` 的重點不是截圖本身，而是 UI 變更後的視覺驗證 loop。

### 學完應能回答

- command、skill、agent 在 OMC 中如何分工？
- `verify` 與 reviewer agent 的關係是什麼？
- `self-improve` 如何把 prompt improvement 變成可評測流程？

## oh-my-codex (OMX)

OMX 是 Codex-oriented enhancer。它的重點是把 agent 行為結構化：prompt specialist、Prometheus strict、state model、plugin skills 和 team runtime。

### 心智模型

把 OMX 想成「有狀態與結構約束的 prompt/skill 系統」：

```text
skill entry
  -> specialist prompt
  -> state/strict constraints
  -> team/runtime module
  -> verified transition
```

OMX 不只問「要用哪個 agent」，還問「這個 agent 的輸出形狀是否被約束」、「目前處於哪個 state」、「下一步 transition 是否合理」。

### 核心流程

1. 使用者透過 skill 或 mode 進入工作流，例如 `plan`、`team`、`analyze`、`prometheus-strict`。
2. Specialist prompt 提供角色判斷，例如 Architect、Security Reviewer、Planner、Executor。
3. Strict prompts 與 state model 約束輸出形狀與進度。
4. Runtime modules 處理 subagents、team、pipeline、hooks、mcp 等能力。
5. Reviewer 類 prompt 或 state transition 檢查用來減少 drift。

### 先讀

- `oh-my-codex/README.md`
- `oh-my-codex/docs/STATE_MODEL.md`
- `oh-my-codex/prompts/prometheus-strict-oracle.md`
- `oh-my-codex/prompts/prometheus-strict-metis.md`
- `oh-my-codex/prompts/prometheus-strict-momus.md`
- `oh-my-codex/plugins/oh-my-codex/skills/plan/SKILL.md`
- `oh-my-codex/plugins/oh-my-codex/skills/team/SKILL.md`

### 讀檔提示

- 讀 `prompts/*.md` 時，不要只看角色名稱，要看它要求的輸出形狀與限制。
- 讀 plugin skill 時，要找它如何把 prompt 接到使用者 workflow。
- 讀 `docs/STATE_MODEL.md` 時，要注意它如何把自由對話變成可控的狀態轉移。

### 容易誤解

- OMX 的 `prompts/*.md` 很多看起來像 OMC agents，但它們在 Codex 脈絡中更像可插拔 specialist prompt。
- Strict prompt 不等於更聰明，而是犧牲一部分彈性換取穩定性和可驗證性。
- `team` 在 OMX 中不是單純多人協作，而是 Codex workflow 的組織方式。

### 學完應能回答

- Prometheus Strict Oracle、Metis、Momus 的責任差異是什麼？
- State model 如何降低 agent drift？
- OMX 的 prompt specialist 和 OMC 的 agent persona 有何不同？

## oh-my-antigravity (OmA)

OmA 是 consensus + self-learning extension。它用 Director、Consensus 和多個 specialist agent 做規劃與審核，並用 learn hook 把 session 中的經驗寫成本地規則。

### 心智模型

把 OmA 想成「共識決策加本地學習」：

```text
user task
  -> specialist proposals
  -> consensus synthesis
  -> director gate
  -> execution/verification
  -> learn hook writes rules
```

它的重點不是「更多 agent」，而是「不讓單一 agent 的判斷直接成為最終決策」。

### 核心流程

1. 使用者透過 `commands/oma/*.toml` 進入功能，例如 `team-plan`、`team-exec`、`consensus`、`learn`。
2. Specialist agents 提案或執行，例如 Architect、Researcher、Reviewer、Editor。
3. Consensus agent 彙整多方意見。
4. Director agent 做最後 gating。
5. `learn` skill/hook 從 session 萃取可重用規則。

### 先讀

- `oh-my-antigravity/README.md`
- `oh-my-antigravity/context/oma-core.md`
- `oh-my-antigravity/agents/director.md`
- `oh-my-antigravity/agents/consensus.md`
- `oh-my-antigravity/skills/learn/SKILL.md`
- `oh-my-antigravity/hooks/scripts/learn.js`

### 讀檔提示

- 讀 agent 時，先判斷它是在產生提案、審核提案、執行任務，還是做最後決策。
- 讀 `commands/oma/*.toml` 時，要看它把哪些 agent/skill 串成使用者入口。
- 讀 learn hook 時，要關注它保存什麼、何時觸發、如何回到後續 session。

### 容易誤解

- Consensus 不是投票器而已，它負責合成與消除衝突。
- Director 不只是 reviewer，它是 gatekeeper，決定是否允許進入執行。
- Learn hook 不是一般 memory，它偏向把可重用工作經驗變成本地 rule。

### 學完應能回答

- Consensus 與 Director 的差異是什麼？
- OmA 的 learn 機制和 OMC self-improve 有何不同？
- OmA 的安全性來自 prompt 嚴格化，還是來自決策流程？

## 專案閱讀順序建議

如果你只有一天：

1. 讀 OMO 的 `src/agents/AGENTS.md` 和 `src/tools/AGENTS.md`。
2. 讀 OMC 的 `docs/ARCHITECTURE.md` 和 `skills/self-improve/SKILL.md`。
3. 讀 OMX 的 `docs/STATE_MODEL.md` 和 `prompts/prometheus-strict-oracle.md`。
4. 讀 OmA 的 `agents/consensus.md`、`agents/director.md`、`skills/learn/SKILL.md`。

如果你要深入研究：

1. 每個專案先讀 README 和 core architecture/context。
2. 再讀核心 workflow 入口：commands 或 skills。
3. 再讀 specialist roles：agents 或 prompts。
4. 最後讀 runtime implementation：tools、hooks、src modules。
