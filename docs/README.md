# ohmyxxx Study Docs

這組文件用來理解四個 agentic coding enhancer 專案：

- `oh-my-openagent` (OMO)
- `oh-my-claudecode` (OMC)
- `oh-my-codex` (OMX)
- `oh-my-antigravity` (OmA)

文件目標不是取代各專案 README，而是把 graphify 找出的 agent、skill、tool、command、hook、prompt 關係整理成可閱讀的學習路線。每章都採教材式寫法：先建立概念，再看原始路徑，最後用自測問題檢查理解。

## 建議閱讀順序

1. [Architecture Map](./01-architecture-map.md)
   先建立四個專案的總體定位，以及 graphify community 如何分群。

2. [Project Guides](./02-project-guides.md)
   逐一理解 OMO、OMC、OMX、OmA 的架構、流程和主要入口。

3. [Agent Skill Tool Map](./03-agent-skill-tool-map.md)
   查每個專案的主要 agent / skill / tool / command / hook / prompt，並用 Planner、Executor、Reviewer、Gatekeeper 等角色分類理解。

4. [Comparisons](./04-comparisons.md)
   橫向比較四個專案在規劃、執行、驗證、安全、學習機制上的差異。

5. [Study Plan](./05-study-plan.md)
   依照 10 步驟閱讀與提問，逐步建立完整理解，並附筆記模板和 NotebookLM / LLM 提問範本。

## 一句話定位

| 專案 | 定位 | 先理解的核心 |
| --- | --- | --- |
| OMO | 多模型、多 agent runtime | agents、tools、hooks 如何形成執行環境 |
| OMC | Claude Code developer OS | commands 和 skills 如何包裝開發生命週期 |
| OMX | schema-constrained Codex enhancer | prompts、skills、state model 如何約束代理行為 |
| OmA | consensus + self-learning extension | agents、skills、hooks 如何支援共識與學習 |

## 資料來源

主要資料來自：

- `graphify-out/graph.json`
- `graphify-out/GRAPH_REPORT.md`
- `graphify-out/FOUR_PROJECTS_DEEP_DIVE.md`
- `graphify-out/NOTEBOOK_LM_STUDY_GUIDE.md`
- 四個專案自己的 `README.md`、`AGENTS.md`、`agents/`、`skills/`、`prompts/`、`tools/`、`hooks/`、`commands/`

文件中提到的 graphify 推論關係應視為分析線索，不等於上游作者明確宣告的設計事實。
