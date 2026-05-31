# Study Plan

這是一個 10 步驟閱讀計畫。每一步都包含學習目標、閱讀材料、預期產出與自測問題。建議一邊讀一邊做筆記，不要一次把所有原始文件讀完。

## 筆記模板

每讀完一個 agent、skill、tool、hook 或 prompt，用同一個模板記錄：

```text
名稱：
來源路徑：
類別：Agent / Prompt / Skill / Tool / Hook / Command
它解決的問題：
它的輸入：
它的輸出或產物：
它依賴哪些其他構件：
它的安全/驗證機制：
我還不確定的地方：
```

## Step 1: 建立全局圖

學習目標：

- 知道四個專案的定位。
- 知道 graphify community 代表什麼。
- 能說出 runtime、lifecycle、structured prompt、consensus learning 的差異。

閱讀：

- `docs/README.md`
- `docs/01-architecture-map.md`
- `graphify-out/GRAPH_REPORT.md`

預期產出：

- 一張四欄比較表：OMO、OMC、OMX、OmA。
- 一句話描述每個專案。

自測：

- 四個專案分別解決什麼問題？
- graphify 的 community 如何對應到四個專案？
- 哪些節點是跨專案核心概念？

## Step 2: 先讀 OMO runtime

學習目標：

- 理解 agent runtime 的基本構造。
- 分清楚 agent、tool、hook 的責任。

閱讀：

- `oh-my-openagent/src/agents/AGENTS.md`
- `oh-my-openagent/src/tools/AGENTS.md`
- `oh-my-openagent/src/hooks/AGENTS.md`

預期產出：

- 畫出 OMO 的任務流：task -> orchestrator -> specialist -> tool -> hook。
- 列出三個最重要的 OMO tools 和 hooks。

自測：

- OMO 的 agent、tool、hook 分別扮演什麼角色？
- Atlas、Prometheus、Hephaestus 的分工是什麼？
- 哪些 hook 是為了解決長上下文或長任務？

## Step 3: 讀 OMC lifecycle

學習目標：

- 理解 command -> skill -> agent/tool 的流程。
- 知道 OMC 如何把工程任務包成可重複 workflow。

閱讀：

- `oh-my-claudecode/README.md`
- `oh-my-claudecode/docs/ARCHITECTURE.md`
- `oh-my-claudecode/commands/self-improve.md`
- `oh-my-claudecode/commands/verify.md`
- `oh-my-claudecode/commands/project-session-manager.md`
- `oh-my-claudecode/skills/plan/SKILL.md`

預期產出：

- 選一個 command，追出它對應的 skill 或流程。
- 寫出 OMC 的 lifecycle：research、plan、execute、verify、release。

自測：

- OMC 如何把 command 對應到 skill？
- 哪些 skill 是核心開發生命週期？
- `self-improve` 和一般開發 skill 差在哪裡？

## Step 4: 讀 OMX structured prompt system

學習目標：

- 理解 prompt specialist 和 runtime agent 的差異。
- 理解 state model 和 strict prompts 為什麼重要。

閱讀：

- `oh-my-codex/README.md`
- `oh-my-codex/docs/STATE_MODEL.md`
- `oh-my-codex/prompts/prometheus-strict-oracle.md`
- `oh-my-codex/prompts/prometheus-strict-metis.md`
- `oh-my-codex/prompts/prometheus-strict-momus.md`

預期產出：

- 寫出 Oracle、Metis、Momus 的分工。
- 畫出一個簡單 state transition 圖。

自測：

- OMX 為什麼要 strict prompt？
- State model 限制了哪些 agent 行為？
- Prometheus Strict Oracle、Metis、Momus 的差異是什麼？

## Step 5: 讀 OmA consensus loop

學習目標：

- 理解 Consensus 和 Director 的差異。
- 理解 session 後學習如何變成規則。

閱讀：

- `oh-my-antigravity/README.md`
- `oh-my-antigravity/context/oma-core.md`
- `oh-my-antigravity/agents/consensus.md`
- `oh-my-antigravity/agents/director.md`
- `oh-my-antigravity/skills/learn/SKILL.md`

預期產出：

- 畫出 OmA 的流程：specialists -> consensus -> director -> execute -> learn。
- 寫出 learn hook 和一般 memory 的差異。

自測：

- Consensus 和 Director 如何分工？
- Learn skill/hook 把什麼東西變成規則？
- OmA 的 safety model 和 OMX 有什麼不同？

## Step 6: 做 agent 對照

學習目標：

- 分辨同名角色在不同專案中的責任差異。
- 知道哪些角色是 planner、reviewer、executor、gatekeeper。

閱讀：

- `docs/03-agent-skill-tool-map.md`
- `oh-my-claudecode/agents/architect.md`
- `oh-my-codex/prompts/architect.md`
- `oh-my-antigravity/agents/architect.md`

預期產出：

- 一張角色矩陣：Planner、Executor、Reviewer、Researcher、Gatekeeper。
- 比較 OMC Architect、OMX Architect、OmA Architect。

自測：

- 三個 Architect 類角色的輸出責任有何差異？
- 哪些 agent 是 planner，哪些是 reviewer，哪些是 executor？
- runtime agent 和 prompt persona 如何區分？

## Step 7: 做 skill 對照

學習目標：

- 理解 skill 作為 workflow entrypoint 的設計。
- 比較 `team`、`ralplan`、`plan` 等跨專案概念。

閱讀：

- `oh-my-claudecode/skills/team/SKILL.md`
- `oh-my-codex/plugins/oh-my-codex/skills/team/SKILL.md`
- `oh-my-antigravity/skills/ralplan/SKILL.md`
- `oh-my-claudecode/skills/ralplan/SKILL.md`

預期產出：

- 一張 `team` 與 `ralplan` 的跨專案對照表。
- 標出哪些 skill 是入口型、支援型、審核型。

自測：

- `team` 和 `ralplan` 在不同專案中的任務邊界是什麼？
- 哪些 skill 是入口，哪些 skill 是支援型？
- 哪些 skill 會啟動多 agent 協作？

## Step 8: 做 tool/hook 對照

學習目標：

- 理解 tool 和 hook 如何改變 agent runtime。
- 分辨安全 hook、上下文 hook、學習 hook。

閱讀：

- `oh-my-openagent/src/tools/delegate-task/AGENTS.md`
- `oh-my-openagent/src/tools/background-task/AGENTS.md`
- `oh-my-openagent/src/hooks/compaction-context-injector/AGENTS.md`
- `oh-my-antigravity/hooks/scripts/learn.js`

預期產出：

- 一張 tool/hook 分類表。
- 寫出 OMO context hook 和 OmA learn hook 的差異。

自測：

- OMO 的 tool 和 hook 如何改變 runtime 行為？
- OmA 的 learn hook 和 OMO 的 context hook 解決的問題有何不同？
- 哪些 hook 是安全控制，哪些 hook 是上下文控制？

## Step 9: 做橫向比較

學習目標：

- 能用同一組維度比較四個專案。
- 知道不同設計的取捨。

閱讀：

- `docs/04-comparisons.md`
- `graphify-out/FOUR_PROJECTS_DEEP_DIVE.md`
- `graphify-out/NOTEBOOK_LM_STUDY_GUIDE.md`

預期產出：

- 一張設計取捨表。
- 寫出「什麼情境借鑑哪個專案」。

自測：

- 如果要設計新系統，四個專案各自最值得借鑑的是什麼？
- 哪個專案最適合作為 runtime 參考？
- 哪個專案最適合作為 prompt/skill library 參考？

## Step 10: 產出自己的理解

學習目標：

- 把閱讀轉成自己的架構判斷。
- 能提出 hybrid design，而不是只整理清單。

請寫一份短文回答：

- 四個專案的共同問題是什麼？
- 它們的分歧點是什麼？
- 你會如何合併它們的優點？
- 哪些設計應避免直接複製？

建議產出：

- 一張架構圖。
- 一份四專案比較表。
- 一份 hybrid agentic enhancer 設計草案。

## NotebookLM / LLM 提問範本

理解型：

- 「請用一張表比較 OMO、OMC、OMX、OmA 的 agent / skill / tool / hook 差異。」
- 「請解釋 graphify community 0、1、2、3、4 分別代表哪些架構群集。」
- 「請列出四個專案中最核心的 20 個概念，並說明閱讀順序。」

比較型：

- 「請比較 OMC self-improve 和 OmA learn hook 的觸發條件、保存方式、回注方式。」
- 「請比較 OMO 的 runtime hook 和 OMX 的 state model，它們各自如何降低 agent drift？」
- 「請比較 OMC agent persona 和 OMX specialist prompt 的差異。」

設計型：

- 「請根據這些文件，設計一個融合 OMO runtime、OMC lifecycle、OMX strict prompt、OmA consensus learning 的新架構。」
- 「如果我要建立一個長任務 coding agent，應該借鑑 OMO 哪些工具與 hooks？」
- 「如果我要建立一個安全優先的 planning workflow，應該借鑑 OmA 和 OMX 哪些設計？」

批判型：

- 「這四個專案有哪些過度工程化風險？」
- 「哪些概念只是名稱相似，但實作目標不同？」
- 「如果只能保留三個核心能力，這四個專案各自應該保留什麼？」
