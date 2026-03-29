# Agentic Loop

Learn how agentic loops work through simple, clear examples.

學習代理循環（Agentic Loop）如何運作，透過簡單清晰的範例。

## What is an Agentic Loop? / 什麼是代理循環？

An agentic loop is the core execution cycle that powers AI agents. Instead of a single prompt-and-response, the agent operates in a loop:

代理循環是驅動 AI 代理的核心執行週期。不同於單次的提示與回應，代理在一個循環中運作：

```
User Task / 使用者任務
   |
   v
+-----------+
|   Think   | <---+
|   思考    |     |
+-----------+     |
   |              |
   v              |
+-----------+     |
|    Act    |     |
|   行動    |     |
+-----------+     |
   |              |
   v              |
+-----------+     |
|  Observe  | ----+
|   觀察    |
+-----------+
   |
   (done? / 完成？)
   |
   v
 Result / 結果
```

1. **Think / 思考** — The LLM reasons about the current state and decides what to do next. LLM 對目前狀態進行推理，並決定下一步行動。
2. **Act / 行動** — The agent executes a tool call (run code, search the web, read a file, etc.). 代理執行工具呼叫（執行程式碼、搜尋網路、讀取檔案等）。
3. **Observe / 觀察** — The agent reads the result of the action. 代理讀取行動的結果。
4. **Repeat / 重複** — Loop back to Think until the task is complete. 回到思考步驟，直到任務完成。

## Examples / 範例

| # | Example | Concept / 概念 |
|---|---|---|
| 01 | [Basic Call](examples/01_basic_call.py) | Send a prompt to Gemini / 發送提示給 Gemini |
| 02 | [Simple Loop](examples/02_simple_loop.py) | The agentic loop skeleton / 代理循環骨架 |
| 03 | [Tool Use](examples/03_tool_use.py) | Function calling with a calculator / 使用計算機工具 |
| 04 | [Multi Tool](examples/04_multi_tool.py) | Multiple tools, multi-step reasoning / 多工具與多步驟推理 |
| 05 | [Error Recovery](examples/05_error_recovery.py) | Handle failures and retry / 處理失敗與重試 |
| 06 | [Conversation Memory](examples/06_conversation_memory.py) | Stateful multi-turn agent / 有狀態的多輪對話代理 |

## Getting Started / 開始使用

```bash
git clone https://github.com/austinjan/agentic-loop.git
cd agentic-loop
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your Gemini API key
# 編輯 .env 並加入你的 Gemini API 金鑰
```

Run any example:

```bash
python examples/01_basic_call.py
```

## License

MIT
