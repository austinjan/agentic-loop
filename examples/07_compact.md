# Example 07: Compact (Context Compaction) / 範例 07：壓縮（上下文壓縮）

## Core Concept / 核心概念

In Example 06, we passed the **full conversation history** to the model every time. This works — until the conversation gets too long and exceeds the model's context window. When that happens, the API call fails.

在範例 06 中，我們每次都把**完整的對話歷史**傳給模型。這可以運作——直到對話太長，超過模型的上下文窗口。那時 API 呼叫就會失敗。

**Compaction** solves this: when the conversation gets too long, ask the model to **summarize** the older messages into a shorter version, then replace the old messages with that summary. The agent keeps working with a compressed but usable history.

**壓縮**解決了這個問題：當對話太長時，請模型把較舊的訊息**摘要**成較短的版本，然後用摘要取代舊訊息。代理繼續使用壓縮但可用的歷史。

## Why This Matters / 為什麼這很重要

Every LLM has a finite context window (e.g., Gemini 2.5 Flash has ~1M tokens). In a real agent that runs for many iterations or handles long conversations, you **will** hit this limit. You have two choices:

每個 LLM 都有有限的上下文窗口（例如 Gemini 2.5 Flash 有 ~1M tokens）。在一個運行多次迭代或處理長對話的真實代理中，你**一定會**碰到這個限制。你有兩個選擇：

1. **Crash** when the context overflows / 上下文溢出時**崩潰**
2. **Compact** the history to make room / **壓縮**歷史以騰出空間

This example teaches option 2.

這個範例教的是選項 2。

## How It Works / 運作方式

```
Conversation grows over time:
對話隨時間增長：

Turn 1:  [user] [model]
Turn 2:  [user] [model] [tool] [model]
Turn 3:  [user] [model]
Turn 4:  [user] [model] [tool] [tool] [model]
  ...
Turn 20: Token count approaching limit!
         Token 數量接近限制！

         ┌─────────────────────────┐
         │  COMPACT TRIGGERED      │
         │  壓縮觸發                │
         │                         │
         │  Old messages (1-18)    │
         │  → Summarized into 1   │
         │    short message        │
         │                         │
         │  Recent messages (19-20)│
         │  → Kept as-is          │
         └─────────────────────────┘

After compaction:
壓縮後：

  [summary of turns 1-18] [turn 19] [turn 20]

  Agent continues working with full context awareness
  but much fewer tokens.
  代理繼續工作，保有完整上下文意識，但 token 數量大幅減少。
```

### Step by step / 逐步說明：

1. **Count tokens** after each model response / 每次模型回應後**計算 token 數**
2. **Check threshold** — is the conversation using too many tokens? / **檢查閾值**——對話是否使用了太多 token？
3. If yes, **split** the conversation into old and recent parts / 如果是，把對話**分割**成舊的和近期的部分
4. **Ask the model to summarize** the old part / **請模型摘要**舊的部分
5. **Replace** old messages with the summary / 用摘要**取代**舊訊息
6. **Continue** the loop — the agent doesn't even notice / **繼續**循環——代理甚至不會察覺

## Key Design Decisions / 關鍵設計決策

| Decision / 決策 | Why / 為什麼 |
|---|---|
| Keep recent messages intact / 保留近期訊息不動 | Recent context is most important for coherent responses / 近期上下文對連貫回應最重要 |
| Use the model itself to summarize / 用模型本身來做摘要 | The model knows what's important for the task / 模型知道什麼對任務重要 |
| Use token count, not message count / 用 token 數，不用訊息數 | Messages vary wildly in size; tokens are the real constraint / 訊息大小差異很大；token 才是真正的限制 |
| Compact proactively before overflow / 在溢出之前主動壓縮 | Crashing mid-task is worse than losing some detail / 任務中途崩潰比失去一些細節更糟 |

## Key Takeaway / 重點摘要

Compaction is how real-world agents handle long-running tasks without crashing. It trades some historical detail for the ability to keep going. The pattern is simple: count tokens, summarize when needed, keep recent context intact. This is the same strategy used by production AI tools like Claude Code and Cursor.

壓縮是真實世界的代理處理長時間任務而不崩潰的方式。它用一些歷史細節換取繼續運作的能力。模式很簡單：計算 token、需要時摘要、保留近期上下文。這與 Claude Code 和 Cursor 等生產級 AI 工具使用的策略相同。
