# Example 03: Tool Use / 範例 03：工具使用

## Core Concept / 核心概念

In Example 02, the agent could only **think** — it had no way to interact with the outside world. This example adds **tools**, giving the agent the ability to take actions and observe results.

在範例 02 中，代理只能**思考**——它無法與外部世界互動。這個範例加入了**工具**，讓代理具備採取行動並觀察結果的能力。

Tool use is a **protocol** — a structured conversation between your code and the model. The model doesn't execute anything itself; it sends back a **request** asking you to call a function, and you send back the **result**. Your code is always in control.

工具使用是一個**協議**——你的程式碼與模型之間的結構化對話。模型本身不執行任何東西；它送回一個**請求**，要求你呼叫某個函式，而你把**結果**送回去。你的程式碼始終掌握控制權。

## The Tool Use Protocol / 工具使用協議

The entire flow looks like this:

整個流程如下：

```
Your Code                              Gemini
────────                              ──────
  │                                      │
  │  1. "What is 15% of 280?"           │
  │  + tool schema (calculate)           │
  │  ─────────────────────────────────►  │
  │                                      │  Model reads the question
  │                                      │  and decides it needs a tool
  │  2. function_call:                   │
  │     calculate("280 * 0.15")          │
  │  ◄─────────────────────────────────  │
  │                                      │
  │  Your code runs calculate()          │
  │  and gets result: "42.0"             │
  │                                      │
  │  3. function_response:               │
  │     {"result": "42.0"}               │
  │  ─────────────────────────────────►  │
  │                                      │  Model reads the result
  │                                      │  and decides: done, or
  │                                      │  call another tool?
  │  4. text: "15% of 280 is 42."       │
  │  ◄─────────────────────────────────  │
  │                                      │
  │  No more function_calls →            │
  │  loop ends, return text              │
```

**Key insight: the model NEVER runs your function.** It only outputs a structured request saying "please call this function with these arguments." Your code decides whether to actually execute it.

**關鍵洞察：模型絕對不會執行你的函式。** 它只輸出一個結構化的請求，說「請用這些參數呼叫這個函式」。你的程式碼決定是否真正執行它。

## Three Things You Must Provide / 你必須提供的三件事

### 1. The Tool Function / 工具函式

A regular Python function that does the actual work:

一個做實際工作的普通 Python 函式：

```python
def calculate(expression: str) -> str:
    result = eval(expression, {"__builtins__": {}})
    return str(result)
```

### 2. The Tool Schema (Function Declaration) / 工具結構描述（函式宣告）

A description that tells the model **what the tool does** and **what arguments it accepts**. The model uses this to decide when and how to call the tool — it never sees your actual code.

一段描述，告訴模型**這個工具做什麼**以及**接受什麼參數**。模型用它來決定何時以及如何呼叫工具——它永遠看不到你的實際程式碼。

```python
calculator_declaration = types.FunctionDeclaration(
    name="calculate",
    description="Evaluate a math expression. Examples: '2+3', '15*0.15'",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "expression": types.Schema(
                type=types.Type.STRING,
                description="The math expression to evaluate",
            ),
        },
        required=["expression"],
    ),
)
```

### 3. The Handler (in the loop) / 處理邏輯（在循環中）

Code in your loop that: checks if the model returned a `function_call`, executes the matching function, and sends the result back as a `function_response`.

在循環中的程式碼：檢查模型是否回傳 `function_call`，執行對應的函式，然後將結果作為 `function_response` 送回去。

```python
if response.function_calls:
    # Model wants to call a tool — execute it
    for fc in response.function_calls:
        result = tool_functions[fc.name](**fc.args)

    # Send result back as function_response
    contents.append(types.Content(role="user", parts=[
        types.Part.from_function_response(name=fc.name, response={"result": result})
    ]))
else:
    # No tool call — model is done, return text
    return response.text
```

## What Changed from Example 02 / 與範例 02 的差異

| Example 02 (Simple Loop) | Example 03 (Tool Use) |
|---|---|
| Loop ends when model outputs "FINAL ANSWER:" | Loop ends when model returns **text instead of function_call** |
| Model can only think | Model can **call tools** to get real data |
| Termination by text pattern | Termination by **response type** (text vs function_call) |
| No schema needed | Must declare **tool schema** for each tool |

## How It Works (Step by Step) / 運作方式（逐步說明）

1. **Define** the tool function + its schema / **定義** 工具函式 + 它的結構描述
2. **Register** the schema with `GenerateContentConfig(tools=...)` / **註冊** 結構描述到 `GenerateContentConfig(tools=...)`
3. **Enter the loop** / **進入循環**
4. **Think:** Send contents to Gemini / **思考：** 將 contents 送給 Gemini
5. **Check response type:** / **檢查回應類型：**
   - `response.function_calls` exists → model wants to use a tool / 存在 → 模型想使用工具
   - `response.function_calls` is empty → model is done, has text answer / 為空 → 模型完成了，有文字答案
6. **Act:** Execute the function your code owns / **行動：** 執行你的程式碼中的函式
7. **Observe:** Send `function_response` back to Gemini / **觀察：** 將 `function_response` 送回 Gemini
8. **Repeat** from step 4 / 從步驟 4 **重複**

## Key Takeaway / 重點摘要

Tool use is a **request-response protocol**: the model requests a function call, your code executes it and returns the result. The model never runs code — it only describes what it wants. This separation keeps you in control: you can validate, log, rate-limit, or reject any tool call before executing it.

工具使用是一個**請求-回應協議**：模型請求函式呼叫，你的程式碼執行它並回傳結果。模型從不執行程式碼——它只描述它想要什麼。這種分離讓你保持控制：你可以在執行之前驗證、記錄、限流或拒絕任何工具呼叫。
