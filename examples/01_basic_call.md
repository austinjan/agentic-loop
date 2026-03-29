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
