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
