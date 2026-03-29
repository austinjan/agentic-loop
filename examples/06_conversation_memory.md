# Example 06: Conversation Memory / 範例 06：對話記憶

## Core Concept / 核心概念

All previous examples handle a single task. This example builds a **multi-turn chat agent** — it remembers what you said earlier and builds on it. Ask it to read a file, then ask a follow-up question about the contents, and it knows what you're referring to.

之前所有範例都處理單一任務。這個範例建構了一個**多輪對話代理**——它記住你之前說的，並在此基礎上繼續。請它讀取一個檔案，然後問一個關於內容的後續問題，它知道你在指什麼。

The "memory" is simply the conversation history — the full list of messages passed to the LLM on every call.

「記憶」就是對話歷史——每次呼叫時傳給 LLM 的完整訊息列表。

## How It Works / 運作方式

1. Start an interactive chat loop (`input()` prompt) / 啟動互動式聊天循環（`input()` 提示）
2. Each user message is appended to `contents` / 每條使用者訊息都被加入 `contents`
3. Gemini receives the **full conversation history** on every call / Gemini 每次呼叫都收到**完整的對話歷史**
4. Tool calls are processed in an inner loop / 工具呼叫在內部循環中處理
5. The agent's response is appended to `contents` / 代理的回應被加入 `contents`
6. Next user turn sees everything that came before / 下一個使用者輪次看到之前的所有內容

Example conversation:
```
[You] What files are in the sandbox?
[Agent] There are two files: hello.txt and data.csv
[You] Read the CSV one
[Agent] (reads data.csv, returns contents)
[You] What's the average age?
[Agent] (calculates from remembered data) The average age is 30.
```

## Key Takeaway / 重點摘要

LLMs are stateless — they don't remember anything between calls. "Memory" is an illusion created by passing the full conversation history each time. This is simple but effective, with one caveat: very long conversations will eventually exceed the model's context window.

LLM 是無狀態的——它們在呼叫之間不記得任何事情。「記憶」是每次傳遞完整對話歷史所創造的假象。這很簡單但有效，有一個注意事項：非常長的對話最終會超過模型的上下文窗口。
