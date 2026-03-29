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
