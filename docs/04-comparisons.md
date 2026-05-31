# Comparisons

這章用橫向問題比較四個專案。比較的目的不是選出「最好」的專案，而是理解它們各自把控制點放在哪裡：runtime、lifecycle、schema/state、consensus learning。

主要來源：

- `graphify-out/GRAPH_REPORT.md`
- `graphify-out/FOUR_PROJECTS_DEEP_DIVE.md`
- `docs/03-agent-skill-tool-map.md`
- 四個專案的核心 agents、skills、prompts、tools、hooks

## Orchestration Model

| 專案 | 模型 | 特徵 | 適合借鑑的情境 |
| --- | --- | --- | --- |
| OMO | Hierarchical runtime | Atlas/Prometheus 路由，透過 tools 和 hooks 支援長任務 | 你要做可運行的多 agent 系統 |
| OMC | Command-to-skill lifecycle | command 是入口，skill 是流程，agent 是 specialist | 你要把開發流程產品化 |
| OMX | Structured prompt system | prompt specialist + schema/state 約束 | 你要降低 agent drift 和輸出不穩定 |
| OmA | Consensus director loop | 多 agent 提案，Consensus 合併，Director gatekeeping | 你要多方審核與安全決策 |

看 orchestration model 時，重點是「誰有最終決策權」：

- OMO：orchestrator 和 runtime policy 決定任務流向。
- OMC：command/skill workflow 決定任務步驟。
- OMX：state/strict prompt 決定合法輸出和下一步。
- OmA：Consensus/Director 決定是否收斂並放行。

## Planning

Planning 是四個專案最容易混淆的地方，因為每個專案都有 planner 類角色，但它們的責任邊界不同。

| 專案 | Planning 重點 | 代表項目 | 取捨 |
| --- | --- | --- | --- |
| OMO | runtime 分派與任務分解 | Atlas、Prometheus、Metis | 彈性高，但需要 hook/tool 支撐穩定性 |
| OMC | workflow planning | `plan`、`ralplan`、`self-improve` | 適合工程任務，但較依賴 command/skill 設計 |
| OMX | structured planning | Prometheus Strict Metis、Planner、state model | 穩定、可驗證，但彈性較低 |
| OmA | consensus planning | Consensus、Director、Ralplan | 安全性高，但流程較重 |

判斷方法：

- 如果 planning 會直接 spawn 或 delegate subagent，偏 OMO。
- 如果 planning 是某個 command 的階段，偏 OMC。
- 如果 planning 強調輸出格式和狀態轉移，偏 OMX。
- 如果 planning 需要多方提案與合併，偏 OmA。

## Execution

Execution 比較的是「計畫如何變成行動」。

- OMO：最強調 runtime execution，有 `delegate-task`、`background-task`、tmux/subagent 能力。它適合長時間、多任務、多模型並行。
- OMC：execution 多由 command/skill 指派 agent 或 tool 執行，偏開發工作流，例如 debug、verify、release。
- OMX：execution 受 prompt role 與 runtime module 管理，強調狀態、pipeline、team。
- OmA：execution 在 Director 批准後進行，強調 gatekeeping。

設計取捨：

| 需求 | 優先借鑑 |
| --- | --- |
| 需要背景任務與非同步工作 | OMO |
| 需要標準化工程流程 | OMC |
| 需要每一步可被狀態機檢查 | OMX |
| 需要先審核再執行 | OmA |

## Verification and Safety

| 專案 | 驗證方式 | 安全重點 | 風險 |
| --- | --- | --- | --- |
| OMO | hooks、fallback、task continuation checks | runtime guardrails | hooks 太多時理解成本高 |
| OMC | `verify`、`visual-verdict`、review agents | 開發任務完成度與 UI/測試確認 | command/skill 若設計鬆散，驗證可能不一致 |
| OMX | strict prompts、state model、reviewer prompts | 限制輸出形狀與流程漂移 | 過度 strict 可能降低探索彈性 |
| OmA | Consensus + Director + verifier | 多方審核與最終 gatekeeping | 流程較重，簡單任務可能成本過高 |

安全模型可以分成三種：

- Runtime safety：OMO 代表，靠 hooks 和 fallback 管理執行過程。
- Workflow safety：OMC 代表，靠 verify/review/visual QA 管理任務完成度。
- Decision safety：OMX/OmA 代表，靠 strict/state 或 consensus/director 管理決策品質。

## Context and Memory

上下文問題是 agentic coding 的核心瓶頸。四個專案各自解法不同。

| 專案 | 解法 | 主要用途 |
| --- | --- | --- |
| OMO | context recovery、compaction injector、session recovery | 長任務不中斷、壓縮上下文 |
| OMC | memory/wiki/session/state tools | 保存專案知識與工作狀態 |
| OMX | state model、runtime state、wiki/ralph | 管理流程狀態與持續任務 |
| OmA | learn hook | 把 session 經驗轉成 reusable rules |

要分清楚三個概念：

- Context compaction：把目前對話/任務壓縮，讓同一任務繼續。
- Memory/wiki：保存可查詢知識，支援後續任務。
- Learned rule：把成功經驗轉成未來 session 的行為準則。

## Self-Improvement

| 專案 | 自我改善型態 | 觀察重點 |
| --- | --- | --- |
| OMO | runtime recovery 和 prompt/hook feedback | 如何從錯誤與 context limit 中恢復 |
| OMC | `self-improve` benchmark builder | 如何把改善目標變成可評測實驗 |
| OMX | prompt/skill bloat audit、strict workflow、state model | 如何用結構化約束改善穩定性 |
| OmA | `/oma:learn` 從 session history 萃取本地規則 | 如何把一次解法變成後續規則 |

OMC 和 OmA 都像「學習」，但方向不同：

- OMC self-improve 偏實驗與評測，問的是「怎樣證明 prompt/workflow 變好了？」
- OmA learn 偏經驗萃取，問的是「這次解掉的問題是否能變成以後可用的規則？」

## Extensibility

| 面向 | OMO | OMC | OMX | OmA |
| --- | --- | --- | --- | --- |
| 新增角色 | 加 agent docs/registry | 加 `agents/*.md` | 加 `prompts/*.md` | 加 `agents/*.md` |
| 新增工作流 | 加 tools/hooks/features | 加 command + skill | 加 plugin skill + prompt/state | 加 command + skill + agent |
| 新增保護 | 加 hook | 加 verify/review skill | 加 strict prompt/state check | 加 Director/Consensus rule |
| 新增記憶 | context/session feature | memory/wiki tools | state/wiki/ralph | learn/rules |

如果你要設計自己的系統，先決定擴充點：

- 想讓使用者多一個命令：學 OMC/OmA。
- 想讓 agent 多一種工具：學 OMO。
- 想讓輸出更穩：學 OMX。
- 想讓決策更保守：學 OmA。

## 如果要借鑑設計

| 目標 | 優先看 | 不建議直接照抄的部分 |
| --- | --- | --- |
| 做多 agent runtime | OMO | 不要一開始就複製所有 hooks |
| 做開發工作流 command/skill | OMC | 不要讓 command 只是薄 alias |
| 限制 agent 輸出與流程漂移 | OMX | 不要過早把所有任務 strict 化 |
| 做共識規劃與 gatekeeping | OmA | 不要把簡單任務也變成重流程 |
| 做 context compaction/recovery | OMO | 不要只壓縮文字，還要保留任務狀態 |
| 做 UI 視覺驗證 | OMC | 不要只截圖，要定義判斷標準 |
| 做 session 後學習 | OmA | 不要把所有 session 都寫成規則 |
| 做 prompt specialist library | OMX + OMC | 不要只複製角色名稱，要複製輸出責任 |

## 常見混淆

- `agent` 不一定都是 runtime process：OMX 的 `prompts/*.md` 更像 specialist prompt；OMO 的 agent 更接近 runtime role。
- `skill` 不一定等於 tool：skill 多半是 workflow instruction；tool 通常有實作與 I/O。
- `team` 在各專案語意不同：OMO 偏 runtime coordination，OMC 偏 coordinated execution，OMX 偏 Codex team workflow，OmA 偏 consensus team mode。
- `ralph`/loop 類概念應按專案讀：它們共享持續性/長任務脈絡，但不是同一套實作。
- `strict` 不等於安全的全部：OMX 透過 strict 限制形狀，OmA 透過共識和 gatekeeping 限制決策。

## 自測問題

- 如果你要做一個需要跑 30 分鐘的背景 agent，哪個專案最值得先讀？為什麼？
- 如果你要設計一個「先研究、再規劃、再驗證」的工程 command，哪個專案最值得先讀？
- 如果你擔心 agent 任意跳步，OMX 和 OmA 各自怎麼解？
- OMC self-improve 和 OmA learn 都能「改善未來表現」，但它們保存的東西有何不同？
