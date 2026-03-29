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
