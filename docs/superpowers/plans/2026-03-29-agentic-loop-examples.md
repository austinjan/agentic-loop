# Agentic Loop Learning Examples — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 6 progressive Python examples that teach agentic loop patterns using Google Gemini.

**Architecture:** Each example is a standalone `.py` file with a companion `.md` doc. No shared modules. All tools defined inline. Bilingual comments (English + Traditional Chinese).

**Tech Stack:** Python 3.10+, `google-genai`, `python-dotenv`

---

### Task 1: Project Scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `examples/sandbox/hello.txt`
- Create: `examples/sandbox/data.csv`
- Modify: `README.md`

- [ ] **Step 1: Create `requirements.txt`**

```
google-genai
python-dotenv
```

- [ ] **Step 2: Create `.env.example`**

```
GEMINI_API_KEY=your-api-key-here
```

- [ ] **Step 3: Create `.gitignore`**

```
.env
__pycache__/
*.pyc
.venv/
```

- [ ] **Step 4: Create `examples/sandbox/hello.txt`**

```
Hello, World!
This is a sample file for the agentic loop examples.
You can ask the agent to read this file.
```

- [ ] **Step 5: Create `examples/sandbox/data.csv`**

```csv
name,age,city
Alice,30,Taipei
Bob,25,Tokyo
Charlie,35,Seoul
```

- [ ] **Step 6: Update `README.md`**

Replace the existing README with:

```markdown
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
```

- [ ] **Step 7: Commit**

```bash
git add requirements.txt .env.example .gitignore examples/sandbox/ README.md
git commit -m "feat: add project scaffolding and update README"
```

---

### Task 2: Example 01 — Basic Call

**Files:**
- Create: `examples/01_basic_call.py`
- Create: `examples/01_basic_call.md`

- [ ] **Step 1: Create `examples/01_basic_call.py`**

```python
"""
Example 01: Basic Call
Send a single prompt to Gemini and print the response.

範例 01：基本呼叫
發送一個提示給 Gemini 並印出回應。
"""

import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
# 從 .env 檔案載入環境變數
load_dotenv()

# Create a Gemini client with your API key
# 使用你的 API 金鑰建立 Gemini 客戶端
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# The model to use for generation
# 用於生成的模型
MODEL = "gemini-2.5-flash"


def main():
    # Define a simple prompt
    # 定義一個簡單的提示
    prompt = "Explain what an AI agent is in 3 sentences."

    print(f"[Prompt] {prompt}")
    print("-" * 40)

    # Send the prompt to Gemini and get the response
    # 發送提示給 Gemini 並取得回應
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    # Print the response text
    # 印出回應文字
    print(f"[Response] {response.text}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Create `examples/01_basic_call.md`**

```markdown
# Example 01: Basic Call / 範例 01：基本呼叫

## Core Concept / 核心概念

This example demonstrates the simplest interaction with an LLM: send a prompt, get a response. This is the foundation everything else builds on. Before we can build a loop, we need to understand the single call.

這個範例展示了與 LLM 最簡單的互動：發送提示，取得回應。這是所有後續範例的基礎。在建構循環之前，我們需要先了解單次呼叫。

## How It Works / 運作方式

1. Load the API key from environment variables / 從環境變數載入 API 金鑰
2. Create a Gemini client / 建立 Gemini 客戶端
3. Send a text prompt using `generate_content()` / 使用 `generate_content()` 發送文字提示
4. Print the response / 印出回應

This is a **one-shot** interaction — no loop, no tools, no memory.
這是一次**單次**互動——沒有循環、沒有工具、沒有記憶。

## Key Takeaway / 重點摘要

An LLM API call is just a function call: input text in, output text out. The agentic loop wraps this simple call in a cycle that enables multi-step reasoning.

LLM API 呼叫就是一個函式呼叫：文字輸入，文字輸出。代理循環將這個簡單的呼叫包裝在一個循環中，使多步驟推理成為可能。
```

- [ ] **Step 3: Run example to verify it works**

Run: `cd examples && python 01_basic_call.py`
Expected: Prints a prompt and a response from Gemini.

- [ ] **Step 4: Commit**

```bash
git add examples/01_basic_call.py examples/01_basic_call.md
git commit -m "feat: add example 01 — basic Gemini call"
```

---

### Task 3: Example 02 — Simple Loop

**Files:**
- Create: `examples/02_simple_loop.py`
- Create: `examples/02_simple_loop.md`

- [ ] **Step 1: Create `examples/02_simple_loop.py`**

```python
"""
Example 02: Simple Loop
The core agentic loop — Think, Decide, Repeat — without any tools.

範例 02：簡單循環
核心代理循環——思考、決定、重複——不使用任何工具。
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
# 從 .env 檔案載入環境變數
load_dotenv()

# Create a Gemini client
# 建立 Gemini 客戶端
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"

# Maximum number of loop iterations to prevent infinite loops
# 最大循環次數，防止無限循環
MAX_ITERATIONS = 10


def run_agent(task: str):
    """
    Run the agentic loop for a given task.
    對給定任務執行代理循環。
    """
    print(f"[Task] {task}")
    print("=" * 50)

    # System instruction that tells the model how to behave as an agent
    # 系統指令，告訴模型如何作為代理運作
    system_instruction = """You are a step-by-step reasoning agent. Break down the task and think through it step by step.

For each step:
1. State what you're thinking about
2. Provide your reasoning
3. State your conclusion for this step

When you have reached the final answer, start your response with "FINAL ANSWER:" followed by your complete answer.

Do not output "FINAL ANSWER:" until you are fully done reasoning."""

    # Build the conversation history
    # 建構對話歷史
    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=task)],
        )
    ]

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
    )

    for i in range(MAX_ITERATIONS):
        print(f"\n--- Iteration {i + 1} ---")

        # Think: ask the model to reason about the current state
        # 思考：請模型對目前狀態進行推理
        print("[Think] Asking Gemini to reason...")
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        response_text = response.text
        print(f"[Response]\n{response_text}")

        # Decide: check if the model has reached a final answer
        # 決定：檢查模型是否已達到最終答案
        if "FINAL ANSWER:" in response_text:
            print("\n" + "=" * 50)
            print("[Done] Agent has reached a final answer.")
            final_answer = response_text.split("FINAL ANSWER:")[-1].strip()
            print(f"[Final Answer] {final_answer}")
            return final_answer

        # Append model response and prompt it to continue
        # 加入模型回應並提示它繼續
        contents.append(response.candidates[0].content)
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part(text="Continue your reasoning. If you have reached the final answer, start with 'FINAL ANSWER:'")],
            )
        )

    print("\n[Warning] Max iterations reached without a final answer.")
    print("警告：已達最大循環次數，但未得到最終答案。")
    return None


def main():
    # A task that requires multi-step reasoning
    # 一個需要多步驟推理的任務
    task = "What is 15% of 280, then add 42 to the result?"
    run_agent(task)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Create `examples/02_simple_loop.md`**

```markdown
# Example 02: Simple Loop / 範例 02：簡單循環

## Core Concept / 核心概念

This example introduces the **agentic loop** — the repeating cycle of Think → Decide → Repeat. The agent doesn't have any tools yet; it just reasons step by step until it reaches a final answer.

這個範例介紹了**代理循環**——思考 → 決定 → 重複的循環週期。代理還沒有任何工具；它只是逐步推理，直到得出最終答案。

The key insight: instead of asking for one big answer, we let the model iterate. Each loop gives it a chance to refine its thinking.

核心洞察：我們不是要求一個大答案，而是讓模型反覆迭代。每次循環都給它一個機會來精煉思考。

## How It Works / 運作方式

1. Define a task and a system instruction that tells Gemini to reason step by step / 定義任務和系統指令，告訴 Gemini 逐步推理
2. Enter the loop (max 10 iterations) / 進入循環（最多 10 次迭代）
3. **Think:** Send the conversation to Gemini / **思考：** 將對話發送給 Gemini
4. **Decide:** Check if the response contains "FINAL ANSWER:" / **決定：** 檢查回應是否包含 "FINAL ANSWER:"
5. If not done, append the response and ask Gemini to continue / 如果未完成，加入回應並要求 Gemini 繼續
6. If done, extract and return the final answer / 如果完成，提取並回傳最終答案

## Key Takeaway / 重點摘要

The agentic loop is just a `while` loop around an LLM call. The "intelligence" comes from the model — the loop just gives it room to think in steps. The termination condition ("FINAL ANSWER:") prevents infinite loops.

代理循環就是在 LLM 呼叫外面包一個 `while` 循環。「智慧」來自模型——循環只是給它空間分步思考。終止條件（"FINAL ANSWER:"）防止無限循環。
```

- [ ] **Step 3: Run example to verify it works**

Run: `cd examples && python 02_simple_loop.py`
Expected: Prints multiple iterations of reasoning, then a final answer.

- [ ] **Step 4: Commit**

```bash
git add examples/02_simple_loop.py examples/02_simple_loop.md
git commit -m "feat: add example 02 — simple agentic loop"
```

---

### Task 4: Example 03 — Tool Use

**Files:**
- Create: `examples/03_tool_use.py`
- Create: `examples/03_tool_use.md`

- [ ] **Step 1: Create `examples/03_tool_use.py`**

```python
"""
Example 03: Tool Use
Add a calculator tool that the agent can call during its reasoning loop.

範例 03：工具使用
加入一個計算機工具，讓代理在推理循環中呼叫。
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
# 載入環境變數
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"
MAX_ITERATIONS = 10


# --- Tool definitions ---
# --- 工具定義 ---

def calculate(expression: str) -> str:
    """
    Evaluate a math expression and return the result.
    計算數學表達式並回傳結果。
    """
    try:
        # Only allow safe math operations
        # 只允許安全的數學運算
        allowed_names = {"__builtins__": {}}
        result = eval(expression, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


# Define the tool schema for Gemini
# 為 Gemini 定義工具結構描述
calculator_declaration = {
    "name": "calculate",
    "description": "Evaluate a math expression. Examples: '2 + 3', '15 * 0.15', '100 / 4'. Returns the numeric result.",
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The math expression to evaluate, e.g. '2 + 3 * 4'",
            },
        },
        "required": ["expression"],
    },
}


# Map of tool names to their implementations
# 工具名稱對應到實作的映射
tool_functions = {
    "calculate": calculate,
}


def run_agent(task: str):
    """
    Run the agentic loop with tool use.
    執行帶有工具使用的代理循環。
    """
    print(f"[Task] {task}")
    print("=" * 50)

    # Configure tools for the model
    # 為模型配置工具
    tools = types.Tool(function_declarations=[calculator_declaration])
    config = types.GenerateContentConfig(
        tools=[tools],
        # Disable automatic function calling so we control the loop
        # 停用自動函式呼叫，讓我們控制循環
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=task)],
        )
    ]

    for i in range(MAX_ITERATIONS):
        print(f"\n--- Iteration {i + 1} ---")

        # Think: send conversation to Gemini
        # 思考：將對話發送給 Gemini
        print("[Think] Asking Gemini...")
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        # Check if the model wants to call a tool
        # 檢查模型是否想要呼叫工具
        if response.function_calls:
            # Append the model's response (contains the function call)
            # 加入模型的回應（包含函式呼叫）
            contents.append(response.candidates[0].content)

            # Process each function call
            # 處理每個函式呼叫
            function_response_parts = []
            for fc in response.function_calls:
                print(f"[Tool Call] {fc.name}({dict(fc.args)})")

                # Act: execute the tool
                # 行動：執行工具
                func = tool_functions[fc.name]
                result = func(**fc.args)
                print(f"[Tool Result] {result}")

                # Build the function response
                # 建構函式回應
                function_response_parts.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response={"result": result},
                    )
                )

            # Observe: send the tool results back to Gemini
            # 觀察：將工具結果發送回 Gemini
            contents.append(
                types.Content(role="user", parts=function_response_parts)
            )

        else:
            # No tool call — the model has produced a final text response
            # 沒有工具呼叫——模型已產生最終文字回應
            print(f"\n[Done] {response.text}")
            return response.text

    print("\n[Warning] Max iterations reached.")
    return None


def main():
    task = "What is 15% of 280, then add 42 to the result?"
    run_agent(task)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Create `examples/03_tool_use.md`**

```markdown
# Example 03: Tool Use / 範例 03：工具使用

## Core Concept / 核心概念

This example adds **tools** to the agentic loop. The agent can now call a calculator function to perform accurate math, instead of relying on the LLM's internal arithmetic (which can be unreliable).

這個範例在代理循環中加入了**工具**。代理現在可以呼叫計算機函式來進行精確的數學運算，而不是依賴 LLM 內部的算術（可能不可靠）。

This is the heart of what makes an agent an agent: the ability to take actions in the world and observe the results.

這是讓代理成為代理的核心：在世界中採取行動並觀察結果的能力。

## How It Works / 運作方式

1. Define a `calculate()` function and its schema / 定義 `calculate()` 函式及其結構描述
2. Pass the tool schema to Gemini via `GenerateContentConfig` / 透過 `GenerateContentConfig` 將工具結構描述傳給 Gemini
3. Enter the loop / 進入循環
4. **Think:** Gemini reasons about the task / **思考：** Gemini 對任務進行推理
5. **Act:** If Gemini returns a `function_call`, execute the matching function / **行動：** 如果 Gemini 回傳 `function_call`，執行對應的函式
6. **Observe:** Send the function result back to Gemini / **觀察：** 將函式結果發送回 Gemini
7. Repeat until Gemini produces a text response (no more tool calls) / 重複直到 Gemini 產生文字回應（不再呼叫工具）

## Key Takeaway / 重點摘要

Tools extend what an agent can do beyond pure text generation. The pattern is always the same: define the tool, let the LLM decide when to use it, execute it, and feed the result back. The LLM is the brain; tools are the hands.

工具擴展了代理在純文字生成之外的能力。模式始終相同：定義工具、讓 LLM 決定何時使用它、執行它、將結果回傳。LLM 是大腦；工具是雙手。
```

- [ ] **Step 3: Run example to verify it works**

Run: `cd examples && python 03_tool_use.py`
Expected: Prints tool calls with calculator results, then a final answer.

- [ ] **Step 4: Commit**

```bash
git add examples/03_tool_use.py examples/03_tool_use.md
git commit -m "feat: add example 03 — tool use with calculator"
```

---

### Task 5: Example 04 — Multi Tool

**Files:**
- Create: `examples/04_multi_tool.py`
- Create: `examples/04_multi_tool.md`

- [ ] **Step 1: Create `examples/04_multi_tool.py`**

```python
"""
Example 04: Multi Tool
Multiple tools (calculator + filesystem) with multi-step reasoning.

範例 04：多工具
多個工具（計算機 + 檔案系統）與多步驟推理。
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
# 載入環境變數
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"
MAX_ITERATIONS = 15

# Sandbox directory for filesystem tools — restrict access to this folder
# 檔案系統工具的沙盒目錄——限制只能存取此資料夾
SANDBOX_DIR = os.path.join(os.path.dirname(__file__), "sandbox")


# --- Tool definitions ---
# --- 工具定義 ---

def calculate(expression: str) -> str:
    """
    Evaluate a math expression and return the result.
    計算數學表達式並回傳結果。
    """
    try:
        allowed_names = {"__builtins__": {}}
        result = eval(expression, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def read_file(path: str) -> str:
    """
    Read and return the contents of a file in the sandbox directory.
    讀取並回傳沙盒目錄中檔案的內容。
    """
    # Resolve to absolute path within sandbox
    # 解析為沙盒內的絕對路徑
    full_path = os.path.normpath(os.path.join(SANDBOX_DIR, path))

    # Security check: ensure the path is inside the sandbox
    # 安全檢查：確保路徑在沙盒內
    if not full_path.startswith(os.path.normpath(SANDBOX_DIR)):
        return "Error: Access denied. Can only read files inside the sandbox directory."

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found: {path}"
    except Exception as e:
        return f"Error: {e}"


def list_directory(path: str = ".") -> str:
    """
    List files and folders in a directory within the sandbox.
    列出沙盒內目錄中的檔案和資料夾。
    """
    full_path = os.path.normpath(os.path.join(SANDBOX_DIR, path))

    if not full_path.startswith(os.path.normpath(SANDBOX_DIR)):
        return "Error: Access denied. Can only list directories inside the sandbox."

    try:
        entries = os.listdir(full_path)
        if not entries:
            return "(empty directory)"
        return "\n".join(sorted(entries))
    except FileNotFoundError:
        return f"Error: Directory not found: {path}"
    except Exception as e:
        return f"Error: {e}"


# Tool schemas for Gemini
# Gemini 的工具結構描述
tool_declarations = [
    {
        "name": "calculate",
        "description": "Evaluate a math expression. Examples: '2 + 3', '15 * 0.15', '100 / 4'.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate",
                },
            },
            "required": ["expression"],
        },
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file. The path is relative to the sandbox directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the file, e.g. 'hello.txt' or 'data.csv'",
                },
            },
            "required": ["path"],
        },
    },
    {
        "name": "list_directory",
        "description": "List files and folders in a directory. The path is relative to the sandbox directory. Use '.' for the root sandbox directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the directory, defaults to '.'",
                },
            },
            "required": [],
        },
    },
]

# Map of tool names to their implementations
# 工具名稱對應到實作的映射
tool_functions = {
    "calculate": calculate,
    "read_file": read_file,
    "list_directory": list_directory,
}


def run_agent(task: str):
    """
    Run the agentic loop with multiple tools.
    執行帶有多個工具的代理循環。
    """
    print(f"[Task] {task}")
    print("=" * 50)

    tools = types.Tool(function_declarations=tool_declarations)
    config = types.GenerateContentConfig(
        tools=[tools],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=task)],
        )
    ]

    for i in range(MAX_ITERATIONS):
        print(f"\n--- Iteration {i + 1} ---")

        # Think: send conversation to Gemini
        # 思考：將對話發送給 Gemini
        print("[Think] Asking Gemini...")
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        if response.function_calls:
            contents.append(response.candidates[0].content)

            function_response_parts = []
            for fc in response.function_calls:
                print(f"[Tool Call] {fc.name}({dict(fc.args)})")

                # Act: execute the tool
                # 行動：執行工具
                func = tool_functions[fc.name]
                result = func(**fc.args)
                print(f"[Tool Result] {result}")

                function_response_parts.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response={"result": result},
                    )
                )

            # Observe: send results back
            # 觀察：將結果發送回去
            contents.append(
                types.Content(role="user", parts=function_response_parts)
            )

        else:
            print(f"\n[Done] {response.text}")
            return response.text

    print("\n[Warning] Max iterations reached.")
    return None


def main():
    # A task that requires both filesystem and calculator tools
    # 一個同時需要檔案系統和計算機工具的任務
    task = (
        "Look at the files in the sandbox directory. "
        "Read the data.csv file and calculate the average age of all people listed."
    )
    run_agent(task)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Create `examples/04_multi_tool.md`**

```markdown
# Example 04: Multi Tool / 範例 04：多工具

## Core Concept / 核心概念

This example shows an agent using **multiple tools** to solve a task that requires several steps. The agent must plan its approach: first explore the filesystem, then read a file, then compute a result.

這個範例展示代理使用**多個工具**來解決需要多個步驟的任務。代理必須規劃方法：首先探索檔案系統，然後讀取檔案，最後計算結果。

This is where the loop becomes truly powerful — the agent chains tool calls together, with each step informed by the results of the previous one.

這就是循環真正強大的地方——代理將工具呼叫串連在一起，每一步都根據前一步的結果來決定。

## How It Works / 運作方式

1. Define three tools: `calculate`, `read_file`, `list_directory` / 定義三個工具：`calculate`、`read_file`、`list_directory`
2. Filesystem tools are sandboxed — they can only access `./sandbox/` / 檔案系統工具有沙盒限制——只能存取 `./sandbox/`
3. The agent decides which tools to call and in what order / 代理決定呼叫哪些工具以及順序
4. Typical flow: `list_directory` → `read_file` → `calculate` / 典型流程：`list_directory` → `read_file` → `calculate`
5. Each tool result feeds into the next reasoning step / 每個工具結果都輸入到下一個推理步驟

## Key Takeaway / 重點摘要

An agent with multiple tools can solve problems that require planning and sequencing. The LLM figures out the order of operations on its own — you just provide the tools and the goal.

擁有多個工具的代理可以解決需要規劃和排序的問題。LLM 自己判斷操作順序——你只需提供工具和目標。
```

- [ ] **Step 3: Run example to verify it works**

Run: `cd examples && python 04_multi_tool.py`
Expected: Agent lists sandbox, reads data.csv, calculates average age, gives final answer (30).

- [ ] **Step 4: Commit**

```bash
git add examples/04_multi_tool.py examples/04_multi_tool.md
git commit -m "feat: add example 04 — multi-tool with filesystem and calculator"
```

---

### Task 6: Example 05 — Error Recovery

**Files:**
- Create: `examples/05_error_recovery.py`
- Create: `examples/05_error_recovery.md`

- [ ] **Step 1: Create `examples/05_error_recovery.py`**

```python
"""
Example 05: Error Recovery
Handle tool failures gracefully — the agent detects errors and adjusts its approach.

範例 05：錯誤恢復
優雅地處理工具失敗——代理偵測錯誤並調整方法。
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
# 載入環境變數
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"
MAX_ITERATIONS = 15

SANDBOX_DIR = os.path.join(os.path.dirname(__file__), "sandbox")


# --- Tool definitions ---
# --- 工具定義 ---

def calculate(expression: str) -> str:
    """
    Evaluate a math expression. Returns an error string on failure.
    計算數學表達式。失敗時回傳錯誤字串。
    """
    try:
        allowed_names = {"__builtins__": {}}
        result = eval(expression, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def read_file(path: str) -> str:
    """
    Read a file from the sandbox. Returns an error if the file doesn't exist.
    從沙盒讀取檔案。如果檔案不存在則回傳錯誤。
    """
    full_path = os.path.normpath(os.path.join(SANDBOX_DIR, path))
    if not full_path.startswith(os.path.normpath(SANDBOX_DIR)):
        return "Error: Access denied. Can only read files inside the sandbox directory."
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found: {path}"
    except Exception as e:
        return f"Error: {e}"


def list_directory(path: str = ".") -> str:
    """
    List files in a sandbox directory.
    列出沙盒目錄中的檔案。
    """
    full_path = os.path.normpath(os.path.join(SANDBOX_DIR, path))
    if not full_path.startswith(os.path.normpath(SANDBOX_DIR)):
        return "Error: Access denied. Can only list directories inside the sandbox."
    try:
        entries = os.listdir(full_path)
        if not entries:
            return "(empty directory)"
        return "\n".join(sorted(entries))
    except FileNotFoundError:
        return f"Error: Directory not found: {path}"
    except Exception as e:
        return f"Error: {e}"


tool_declarations = [
    {
        "name": "calculate",
        "description": "Evaluate a math expression. Examples: '2 + 3', '15 * 0.15', '100 / 4'.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate",
                },
            },
            "required": ["expression"],
        },
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file. The path is relative to the sandbox directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the file, e.g. 'hello.txt'",
                },
            },
            "required": ["path"],
        },
    },
    {
        "name": "list_directory",
        "description": "List files and folders in a directory relative to the sandbox.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the directory, defaults to '.'",
                },
            },
            "required": [],
        },
    },
]

tool_functions = {
    "calculate": calculate,
    "read_file": read_file,
    "list_directory": list_directory,
}


def run_agent(task: str):
    """
    Run the agentic loop with error recovery.
    執行帶有錯誤恢復的代理循環。
    """
    print(f"[Task] {task}")
    print("=" * 50)

    # System instruction that encourages the agent to handle errors
    # 系統指令，鼓勵代理處理錯誤
    system_instruction = """You are a helpful agent with access to tools. Use them to complete the task.

If a tool returns an error:
- Read the error message carefully
- Think about what went wrong
- Try a different approach (e.g., list the directory first to find the correct filename)
- Do NOT repeat the exact same call that failed

Always explain your reasoning before and after using tools."""

    tools = types.Tool(function_declarations=tool_declarations)
    config = types.GenerateContentConfig(
        tools=[tools],
        system_instruction=system_instruction,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=task)],
        )
    ]

    for i in range(MAX_ITERATIONS):
        print(f"\n--- Iteration {i + 1} ---")

        print("[Think] Asking Gemini...")
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        if response.function_calls:
            contents.append(response.candidates[0].content)

            function_response_parts = []
            for fc in response.function_calls:
                print(f"[Tool Call] {fc.name}({dict(fc.args)})")

                # Act: execute the tool
                # 行動：執行工具
                func = tool_functions[fc.name]
                result = func(**fc.args)

                # Highlight errors so the learner can see the recovery in action
                # 標示錯誤，讓學習者看到錯誤恢復的過程
                if result.startswith("Error:"):
                    print(f"[Tool Error] {result}")
                else:
                    print(f"[Tool Result] {result}")

                function_response_parts.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response={"result": result},
                    )
                )

            # Observe: send results back (including errors)
            # 觀察：將結果發送回去（包括錯誤）
            contents.append(
                types.Content(role="user", parts=function_response_parts)
            )

        else:
            print(f"\n[Done] {response.text}")
            return response.text

    print("\n[Warning] Max iterations reached.")
    return None


def main():
    # This task intentionally references a wrong filename
    # The agent should fail, discover the correct name, and recover
    # 這個任務故意引用了錯誤的檔名
    # 代理應該失敗、發現正確名稱並恢復
    task = (
        "Read the file called 'people.csv' from the sandbox and tell me "
        "the names of everyone listed. If that file doesn't exist, look "
        "for similar files and try those instead."
    )
    run_agent(task)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Create `examples/05_error_recovery.md`**

```markdown
# Example 05: Error Recovery / 範例 05：錯誤恢復

## Core Concept / 核心概念

Real-world tools fail. Files don't exist, calculations have division by zero, APIs time out. A good agent doesn't just crash — it **observes the error, reasons about it, and tries a different approach**.

現實世界中的工具會失敗。檔案不存在、計算遇到除以零、API 逾時。好的代理不會直接崩潰——它會**觀察錯誤、推理原因，並嘗試不同的方法**。

This example is identical to Example 04 in structure, but the task intentionally triggers an error. The interesting part is watching the agent recover.

這個範例在結構上與範例 04 相同，但任務故意觸發了一個錯誤。有趣的部分是觀察代理如何恢復。

## How It Works / 運作方式

1. The task asks for `people.csv` — which doesn't exist / 任務要求 `people.csv`——但它不存在
2. `read_file` returns an error string / `read_file` 回傳錯誤字串
3. The error is sent back to Gemini as a normal tool result / 錯誤作為普通工具結果發送回 Gemini
4. Gemini sees the error, reasons about it, and tries `list_directory` / Gemini 看到錯誤，推理後嘗試 `list_directory`
5. Gemini discovers `data.csv`, reads it, and completes the task / Gemini 發現 `data.csv`，讀取它，完成任務

The key: **errors are just data**. We don't need special error handling logic — the LLM handles it through natural reasoning.

關鍵：**錯誤只是資料**。我們不需要特殊的錯誤處理邏輯——LLM 透過自然推理來處理。

## Key Takeaway / 重點摘要

Error recovery in an agentic loop is free — you get it just by passing the error message back to the LLM. The system instruction nudges the model to try alternative approaches instead of repeating the same failed call.

代理循環中的錯誤恢復是免費的——你只需要將錯誤訊息傳回 LLM。系統指令引導模型嘗試替代方法，而不是重複相同的失敗呼叫。
```

- [ ] **Step 3: Run example to verify it works**

Run: `cd examples && python 05_error_recovery.py`
Expected: Agent tries `people.csv`, gets error, lists directory, finds `data.csv`, reads it, returns names.

- [ ] **Step 4: Commit**

```bash
git add examples/05_error_recovery.py examples/05_error_recovery.md
git commit -m "feat: add example 05 — error recovery"
```

---

### Task 7: Example 06 — Conversation Memory

**Files:**
- Create: `examples/06_conversation_memory.py`
- Create: `examples/06_conversation_memory.md`

- [ ] **Step 1: Create `examples/06_conversation_memory.py`**

```python
"""
Example 06: Conversation Memory
A stateful multi-turn agent that remembers previous interactions.

範例 06：對話記憶
一個有狀態的多輪對話代理，能記住之前的互動。
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
# 載入環境變數
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"
MAX_ITERATIONS = 10

SANDBOX_DIR = os.path.join(os.path.dirname(__file__), "sandbox")


# --- Tool definitions (same as previous examples) ---
# --- 工具定義（與之前的範例相同）---

def calculate(expression: str) -> str:
    """Evaluate a math expression. / 計算數學表達式。"""
    try:
        allowed_names = {"__builtins__": {}}
        result = eval(expression, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def read_file(path: str) -> str:
    """Read a file from the sandbox. / 從沙盒讀取檔案。"""
    full_path = os.path.normpath(os.path.join(SANDBOX_DIR, path))
    if not full_path.startswith(os.path.normpath(SANDBOX_DIR)):
        return "Error: Access denied. Can only read files inside the sandbox directory."
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found: {path}"
    except Exception as e:
        return f"Error: {e}"


def list_directory(path: str = ".") -> str:
    """List files in a sandbox directory. / 列出沙盒目錄中的檔案。"""
    full_path = os.path.normpath(os.path.join(SANDBOX_DIR, path))
    if not full_path.startswith(os.path.normpath(SANDBOX_DIR)):
        return "Error: Access denied. Can only list directories inside the sandbox."
    try:
        entries = os.listdir(full_path)
        if not entries:
            return "(empty directory)"
        return "\n".join(sorted(entries))
    except FileNotFoundError:
        return f"Error: Directory not found: {path}"
    except Exception as e:
        return f"Error: {e}"


tool_declarations = [
    {
        "name": "calculate",
        "description": "Evaluate a math expression. Examples: '2 + 3', '15 * 0.15'.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate",
                },
            },
            "required": ["expression"],
        },
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file relative to the sandbox directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the file",
                },
            },
            "required": ["path"],
        },
    },
    {
        "name": "list_directory",
        "description": "List files and folders in a directory relative to the sandbox.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the directory, defaults to '.'",
                },
            },
            "required": [],
        },
    },
]

tool_functions = {
    "calculate": calculate,
    "read_file": read_file,
    "list_directory": list_directory,
}


def process_tool_calls(response, contents, config):
    """
    Handle the tool-call loop for a single user turn.
    Keep calling tools until the model produces a text response.

    處理單次使用者輪次的工具呼叫循環。
    持續呼叫工具直到模型產生文字回應。
    """
    tools = types.Tool(function_declarations=tool_declarations)

    for _ in range(MAX_ITERATIONS):
        if not response.function_calls:
            # No more tool calls — return the text response
            # 沒有更多工具呼叫——回傳文字回應
            return response

        contents.append(response.candidates[0].content)

        function_response_parts = []
        for fc in response.function_calls:
            print(f"  [Tool Call] {fc.name}({dict(fc.args)})")

            func = tool_functions[fc.name]
            result = func(**fc.args)

            if result.startswith("Error:"):
                print(f"  [Tool Error] {result}")
            else:
                print(f"  [Tool Result] {result}")

            function_response_parts.append(
                types.Part.from_function_response(
                    name=fc.name,
                    response={"result": result},
                )
            )

        contents.append(
            types.Content(role="user", parts=function_response_parts)
        )

        # Get next response (may contain more tool calls or final text)
        # 取得下一個回應（可能包含更多工具呼叫或最終文字）
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

    return response


def main():
    """
    Interactive chat loop — the agent remembers the entire conversation.
    互動式聊天循環——代理記住整段對話。
    """
    print("Agentic Chat (type 'quit' to exit)")
    print("代理聊天（輸入 'quit' 離開）")
    print("=" * 50)

    # System instruction for the chat agent
    # 聊天代理的系統指令
    system_instruction = """You are a helpful assistant with access to tools. You can:
- Calculate math expressions
- Read files from a sandbox directory
- List files in the sandbox directory

Use tools when they help answer the user's question. Remember context from earlier in the conversation.
Be concise in your responses."""

    tools = types.Tool(function_declarations=tool_declarations)
    config = types.GenerateContentConfig(
        tools=[tools],
        system_instruction=system_instruction,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    # Conversation history persists across all user turns
    # 對話歷史在所有使用者輪次中保持
    contents = []

    while True:
        # Get user input
        # 取得使用者輸入
        user_input = input("\n[You] ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye! / 再見！")
            break
        if not user_input:
            continue

        # Add user message to conversation history
        # 將使用者訊息加入對話歷史
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part(text=user_input)],
            )
        )

        # Get response from Gemini
        # 從 Gemini 取得回應
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        # Process any tool calls
        # 處理任何工具呼叫
        response = process_tool_calls(response, contents, config)

        # Add the final response to history
        # 將最終回應加入歷史
        contents.append(response.candidates[0].content)

        print(f"\n[Agent] {response.text}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Create `examples/06_conversation_memory.md`**

```markdown
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
```

- [ ] **Step 3: Run example to verify it works**

Run: `cd examples && python 06_conversation_memory.py`
Expected: Interactive chat. Try: "What files are in the sandbox?" → "Read the CSV" → "What's the average age?" — agent remembers context.

- [ ] **Step 4: Commit**

```bash
git add examples/06_conversation_memory.py examples/06_conversation_memory.md
git commit -m "feat: add example 06 — conversation memory"
```

---

### Task 8: Final Push

- [ ] **Step 1: Push all commits to GitHub**

```bash
git push origin main
```
