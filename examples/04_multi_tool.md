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
