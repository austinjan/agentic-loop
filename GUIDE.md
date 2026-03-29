# Agentic Loop Learning Guide / 代理循環學習指南

This guide walks you through each example: how to run it, what to observe in the output, and what you should learn from it.

本指南帶你逐步了解每個範例：如何執行、如何觀察輸出，以及你應該學到的重點。

---

## Prerequisites / 前置準備

### Option A: Using uv (Recommended) / 使用 uv（推薦）

[uv](https://docs.astral.sh/uv/) is a fast Python package manager that handles Python versions and virtual environments for you.

[uv](https://docs.astral.sh/uv/) 是一個快速的 Python 套件管理器，能自動處理 Python 版本和虛擬環境。

```bash
# Install uv (if not already installed) / 安裝 uv（如果尚未安裝）
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment with Python 3.12 / 建立 Python 3.12 虛擬環境
uv venv --python 3.12

# Activate the virtual environment / 啟動虛擬環境
source .venv/bin/activate

# Install dependencies / 安裝相依套件
uv pip install -r requirements.txt
```

Or run any example directly without activating the venv:

或者不啟動虛擬環境，直接執行任何範例：

```bash
uv run python examples/01_basic_call.py
```

### Option B: Using pip / 使用 pip

```bash
pip install -r requirements.txt
```

### Set up your API key / 設定 API 金鑰

```bash
cp .env.example .env
# Edit .env and paste your Gemini API key
# 編輯 .env 並貼上你的 Gemini API 金鑰
```

Get your Gemini API key from: https://aistudio.google.com/apikey

從這裡取得你的 Gemini API 金鑰：https://aistudio.google.com/apikey

---

## Example 01: Basic Call / 範例 01：基本呼叫

### How to Run / 如何執行

```bash
python examples/01_basic_call.py
```

### What to Observe / 觀察重點

```
[Prompt] Explain what an AI agent is in 3 sentences.
----------------------------------------
[Response] An AI agent is a software system that...
```

You will see:
- `[Prompt]` — the text we sent to Gemini / 我們發送給 Gemini 的文字
- `[Response]` — the text Gemini returned / Gemini 回傳的文字

That's it. One input, one output. No loop, no tools.

就這樣。一個輸入，一個輸出。沒有循環，沒有工具。

### Key Learning / 學習重點

> An LLM API call is just a function call. Everything else we build is layers on top of this simple pattern.
>
> LLM API 呼叫就是一個函式呼叫。我們後續建構的一切，都是在這個簡單模式之上的層層疊加。

---

## Example 02: Simple Loop / 範例 02：簡單循環

### How to Run / 如何執行

```bash
python examples/02_simple_loop.py
```

### What to Observe / 觀察重點

```
[Task] What is 15% of 280, then add 42 to the result?
==================================================

--- Iteration 1 ---
[Think] Asking Gemini to reason...
[Response]
Step 1: I need to calculate 15% of 280...
...

--- Iteration 2 ---
[Think] Asking Gemini to reason...
[Response]
FINAL ANSWER: 84

==================================================
[Done] Agent has reached a final answer.
[Final Answer] 84
```

Pay attention to / 注意觀察：

1. **Multiple iterations** — The agent doesn't answer in one shot. It loops.
   **多次迭代** — 代理不會一次回答。它在循環中運作。

2. **`[Think]` appears each iteration** — Each loop is a new LLM call.
   **每次迭代都出現 `[Think]`** — 每次循環都是一次新的 LLM 呼叫。

3. **"FINAL ANSWER:" triggers exit** — This is the termination condition that stops the loop.
   **"FINAL ANSWER:" 觸發退出** — 這是停止循環的終止條件。

4. **Conversation grows** — Each iteration appends to the history, so Gemini sees all prior reasoning.
   **對話不斷增長** — 每次迭代都加入歷史記錄，所以 Gemini 能看到之前所有的推理。

### Key Learning / 學習重點

> The agentic loop is just a `while` loop around an LLM call. The model provides the intelligence; the loop provides the structure. A clear termination condition prevents infinite loops.
>
> 代理循環就是在 LLM 呼叫外面包一個 `while` 循環。模型提供智慧；循環提供結構。明確的終止條件防止無限循環。

---

## Example 03: Tool Use / 範例 03：工具使用

### How to Run / 如何執行

```bash
python examples/03_tool_use.py
```

### What to Observe / 觀察重點

```
[Task] What is 15% of 280, then add 42 to the result?
==================================================

--- Iteration 1 ---
[Think] Asking Gemini...
[Tool Call] calculate({'expression': '280 * 0.15'})
[Tool Result] 42.0

--- Iteration 2 ---
[Think] Asking Gemini...
[Tool Call] calculate({'expression': '42.0 + 42'})
[Tool Result] 84.0

--- Iteration 3 ---
[Think] Asking Gemini...

[Done] 15% of 280 is 42, and adding 42 gives you 84.
```

Pay attention to / 注意觀察：

1. **`[Tool Call]`** — Gemini decided to call the calculator. We didn't tell it to — the model chose to.
   **`[Tool Call]`** — Gemini 決定呼叫計算機。我們沒有要求它——是模型自己選擇的。

2. **`[Tool Result]`** — We executed the function and sent the result back.
   **`[Tool Result]`** — 我們執行了函式並將結果送回。

3. **Think → Act → Observe cycle** — This is the full agentic loop in action:
   **思考 → 行動 → 觀察 循環** — 這就是完整的代理循環：
   - Think: Gemini reasons about what to do / 思考：Gemini 推理要做什麼
   - Act: Gemini calls the calculator / 行動：Gemini 呼叫計算機
   - Observe: Gemini sees the result / 觀察：Gemini 看到結果

4. **Final text response = done** — When Gemini responds with text instead of a tool call, the loop ends.
   **最終文字回應 = 完成** — 當 Gemini 用文字回應而不是工具呼叫時，循環結束。

### Key Learning / 學習重點

> Tools give the agent hands. The LLM decides *when* and *how* to use them. The pattern is always: define the tool schema → let the LLM call it → execute it → send the result back.
>
> 工具給了代理雙手。LLM 決定*何時*以及*如何*使用它們。模式始終是：定義工具結構 → 讓 LLM 呼叫它 → 執行它 → 將結果送回。

---

## Example 04: Multi Tool / 範例 04：多工具

### How to Run / 如何執行

```bash
python examples/04_multi_tool.py
```

### What to Observe / 觀察重點

```
[Task] Look at the files in the sandbox directory. Read the data.csv file and calculate the average age...
==================================================

--- Iteration 1 ---
[Think] Asking Gemini...
[Tool Call] list_directory({'path': '.'})
[Tool Result] data.csv
hello.txt

--- Iteration 2 ---
[Think] Asking Gemini...
[Tool Call] read_file({'path': 'data.csv'})
[Tool Result] name,age,city
Alice,30,Taipei
Bob,25,Tokyo
Charlie,35,Seoul

--- Iteration 3 ---
[Think] Asking Gemini...
[Tool Call] calculate({'expression': '(30 + 25 + 35) / 3'})
[Tool Result] 30.0

--- Iteration 4 ---
[Think] Asking Gemini...

[Done] The average age of all people listed is 30.
```

Pay attention to / 注意觀察：

1. **Tool sequencing** — The agent figured out the order by itself: list → read → calculate.
   **工具排序** — 代理自己判斷了順序：列出 → 讀取 → 計算。

2. **Multi-step planning** — Each tool result informed the next step. The agent read the CSV, extracted the ages, and built the calculation.
   **多步驟規劃** — 每個工具結果都影響了下一步。代理讀取了 CSV，提取了年齡，並建構了計算。

3. **Three different tools** — The agent chose the right tool for each sub-task.
   **三個不同的工具** — 代理為每個子任務選擇了正確的工具。

### Key Learning / 學習重點

> With multiple tools, the agent becomes a planner. You provide capabilities (tools) and a goal (task) — the LLM determines the strategy. This is the power of the agentic loop: complex tasks decomposed into simple tool calls.
>
> 有了多個工具，代理變成了規劃者。你提供能力（工具）和目標（任務）——LLM 決定策略。這就是代理循環的力量：將複雜任務分解為簡單的工具呼叫。

---

## Example 05: Error Recovery / 範例 05：錯誤恢復

### How to Run / 如何執行

```bash
python examples/05_error_recovery.py
```

### What to Observe / 觀察重點

```
[Task] Read the file called 'people.csv' from the sandbox...
==================================================

--- Iteration 1 ---
[Think] Asking Gemini...
[Tool Call] read_file({'path': 'people.csv'})
[Tool Error] Error: File not found: people.csv     <-- !!

--- Iteration 2 ---
[Think] Asking Gemini...
[Tool Call] list_directory({'path': '.'})
[Tool Result] data.csv
hello.txt

--- Iteration 3 ---
[Think] Asking Gemini...
[Tool Call] read_file({'path': 'data.csv'})
[Tool Result] name,age,city
Alice,30,Taipei
...

--- Iteration 4 ---
[Think] Asking Gemini...

[Done] The names of everyone listed are: Alice, Bob, and Charlie.
```

Pay attention to / 注意觀察：

1. **`[Tool Error]`** — The first attempt fails! `people.csv` doesn't exist.
   **`[Tool Error]`** — 第一次嘗試失敗了！`people.csv` 不存在。

2. **The agent doesn't crash** — It receives the error as normal data and reasons about it.
   **代理沒有崩潰** — 它接收錯誤作為普通資料並進行推理。

3. **Recovery strategy** — The agent lists the directory to find what files actually exist, then reads the correct one.
   **恢復策略** — 代理列出目錄以找到實際存在的檔案，然後讀取正確的檔案。

4. **No special error handling code** — We didn't write any try/catch for recovery. The LLM handles it naturally.
   **沒有特殊的錯誤處理程式碼** — 我們沒有寫任何 try/catch 來恢復。LLM 自然地處理了它。

### Key Learning / 學習重點

> Error recovery is free in an agentic loop. Errors are just data — send them back to the LLM and let it reason about what went wrong. The system instruction nudges the model to try alternatives instead of repeating failures.
>
> 代理循環中的錯誤恢復是免費的。錯誤只是資料——將它們送回 LLM，讓它推理哪裡出了問題。系統指令引導模型嘗試替代方案，而不是重複失敗。

---

## Example 06: Conversation Memory / 範例 06：對話記憶

### How to Run / 如何執行

```bash
python examples/06_conversation_memory.py
```

This is an **interactive** example. Type your messages and press Enter.

這是一個**互動式**範例。輸入你的訊息並按 Enter。

### What to Observe / 觀察重點

Try this conversation / 試試這段對話：

```
[You] What files are in the sandbox?
  [Tool Call] list_directory({'path': '.'})
  [Tool Result] data.csv
hello.txt

[Agent] There are two files: data.csv and hello.txt.

[You] Read the CSV one
  [Tool Call] read_file({'path': 'data.csv'})
  [Tool Result] name,age,city
Alice,30,Taipei
Bob,25,Tokyo
Charlie,35,Seoul

[Agent] The file contains three people: Alice (30, Taipei), Bob (25, Tokyo), Charlie (35, Seoul).

[You] What's the average age?
  [Tool Call] calculate({'expression': '(30 + 25 + 35) / 3'})
  [Tool Result] 30.0

[Agent] The average age is 30.

[You] Who lives in Taipei?
[Agent] Alice lives in Taipei.                     <-- No tool call needed!

[You] quit
Goodbye! / 再見！
```

Pay attention to / 注意觀察：

1. **"Read the CSV one"** — You said "the CSV one", not "data.csv". The agent remembered the previous list and understood the reference.
   **「Read the CSV one」** — 你說的是「the CSV one」而不是「data.csv」。代理記住了之前的列表並理解了指稱。

2. **"What's the average age?"** — The agent used data from a previous turn to build the calculation. It didn't re-read the file.
   **「What's the average age?」** — 代理使用了前一輪的資料來建構計算。它沒有重新讀取檔案。

3. **"Who lives in Taipei?"** — No tool call at all! The agent already has the data in its conversation history.
   **「Who lives in Taipei?」** — 完全沒有工具呼叫！代理已經在對話歷史中有了資料。

4. **Type `quit` to exit** — The chat loop ends gracefully.
   **輸入 `quit` 退出** — 聊天循環優雅地結束。

### Key Learning / 學習重點

> LLMs are stateless — they don't remember anything between calls. "Memory" is created by passing the full conversation history (`contents` list) on every call. This is simple and effective, but long conversations will eventually exceed the model's context window.
>
> LLM 是無狀態的——它們在呼叫之間不記得任何事情。「記憶」是通過每次呼叫時傳遞完整的對話歷史（`contents` 列表）來創建的。這很簡單且有效，但很長的對話最終會超過模型的上下文窗口。

---

## Summary: The Complete Picture / 總結：完整的全貌

After completing all 6 examples, you now understand the full anatomy of an AI agent:

完成所有 6 個範例後，你現在了解了 AI 代理的完整結構：

| # | Concept / 概念 | What You Learned / 你學到了什麼 |
|---|---|---|
| 01 | Basic Call / 基本呼叫 | An LLM call is just a function call / LLM 呼叫只是一個函式呼叫 |
| 02 | Simple Loop / 簡單循環 | Wrap it in a loop for multi-step reasoning / 包在循環中實現多步驟推理 |
| 03 | Tool Use / 工具使用 | Give the agent tools to interact with the world / 給代理工具與世界互動 |
| 04 | Multi Tool / 多工具 | Multiple tools enable planning and sequencing / 多個工具實現規劃與排序 |
| 05 | Error Recovery / 錯誤恢復 | Errors are just data — let the LLM reason about them / 錯誤只是資料——讓 LLM 推理 |
| 06 | Memory / 記憶 | Conversation history creates the illusion of memory / 對話歷史創造記憶的假象 |

### The Core Pattern / 核心模式

Every AI agent, no matter how complex, is built on this loop:

每個 AI 代理，無論多複雜，都建立在這個循環之上：

```
while not done:
    response = llm.call(history)    # Think / 思考
    if response.has_tool_call:
        result = execute(tool_call)  # Act / 行動
        history.append(result)       # Observe / 觀察
    else:
        done = True                  # Finish / 完成
```

That's it. Everything else — tool selection, error recovery, memory, planning — emerges from this simple structure.

就是這樣。其他一切——工具選擇、錯誤恢復、記憶、規劃——都從這個簡單的結構中湧現。
