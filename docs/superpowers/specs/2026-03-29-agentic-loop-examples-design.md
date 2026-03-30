# Agentic Loop Learning Examples — Design Spec

## Overview

A progressive Python tutorial that teaches how agentic loops work using Google Gemini. The project provides 6 numbered, self-contained examples that build from a basic LLM call to a stateful conversational agent with error recovery.

**Goal:** Simple and clear examples that anyone can read top-to-bottom and understand the agentic loop pattern.

## Target Audience

Mixed level — starts from zero (what is an LLM API call?) and progresses to intermediate concepts (error recovery, conversation memory). Each example introduces exactly one new concept.

## Technology

- **Language:** Python
- **LLM Provider:** Google Gemini via `google-genai` SDK
- **Dependencies:** `google-genai`, `python-dotenv` (nothing else)
- **Python version:** 3.10+

## Project Structure

```
agentic-loop/
  README.md                          # Project overview with example index
  requirements.txt                   # google-genai, python-dotenv
  .env.example                       # GEMINI_API_KEY=your-key-here
  examples/
    01_basic_call.py
    01_basic_call.md
    02_simple_loop.py
    02_simple_loop.md
    03_tool_use.py
    03_tool_use.md
    04_multi_tool.py
    04_multi_tool.md
    05_error_recovery.py
    05_error_recovery.md
    06_conversation_memory.py
    06_conversation_memory.md
    sandbox/                         # Sample files for filesystem tool examples
      hello.txt
      data.csv
```

## Example Progression

| # | File | Concept | Description |
|---|---|---|---|
| 01 | `basic_call.py` | Raw LLM call | Send a prompt to Gemini, print the response. No loop. Establishes the API foundation. |
| 02 | `simple_loop.py` | The agentic loop | Agent loops (Think → Decide → Repeat) until Gemini says "DONE". No tools — just the loop skeleton. |
| 03 | `tool_use.py` | Single tool (calculator) | Gemini can call a calculator tool, observe the result, and continue reasoning. Introduces function calling. |
| 04 | `multi_tool.py` | Multiple tools | Adds filesystem tools (read_file, list_directory). Agent solves tasks requiring multiple sequential tool calls. |
| 05 | `error_recovery.py` | Resilience | Tools can fail (file not found, division by zero). Agent detects errors and retries or adjusts its approach. |
| 06 | `conversation_memory.py` | Stateful agent | Message history persists across user turns. Agent remembers prior context in an interactive chat loop. |

## Tool Definitions

### Calculator (introduced in 03)

- `calculate(expression: str) -> str`
- Evaluates a math expression using a restricted safe eval (no imports, no builtins)
- Returns the result as a string, or an error message on failure

### Filesystem (introduced in 04)

- `read_file(path: str) -> str` — reads and returns file contents. Returns error if not found.
- `list_directory(path: str) -> str` — lists files/folders. Defaults to current directory.
- **Read-only.** Restricted to `./sandbox/` directory for safety.

Tools are defined inline in each file as plain Python functions + Gemini function calling schema dicts. No shared module.

## Code Pattern

Every example follows the same structure:

```python
"""
Example N: <Title>
<One-line description>

範例 N：<標題>
<一行描述>
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- Tool definitions (examples 03+) ---
# 工具定義（範例 03 以後）

# --- Agent loop ---
# 代理循環

# --- Main ---
if __name__ == "__main__":
    ...
```

### Code style rules

- **No classes, no abstractions.** Everything is functions and plain data.
- **No shared modules.** Each file is fully self-contained. Duplication is intentional.
- **Comments are bilingual:** English first, then Traditional Chinese on the next line.
- **Print statements** show each loop step: `[Think]`, `[Tool Call]`, `[Tool Result]`, `[Done]` — so learners can follow execution in the terminal.
- **Inline comments explain *why*, not *what*** — the code should be self-explanatory.
- **Each file readable top-to-bottom in under 5 minutes.**
- **Keep everything simple and clear:** Ensure every function name is clear and descriptive.
## Companion Documents

Each example has a `.md` file with the same number prefix. Template:

```markdown
# Example N: <Title> / 範例 N：<標題>

## Core Concept / 核心概念
What this example teaches and why it matters.
這個範例教什麼，以及為什麼重要。

## How It Works / 運作方式
Step-by-step explanation of the code logic.
逐步說明程式碼邏輯。

## Key Takeaway / 重點摘要
The one thing to remember from this example.
這個範例最重要的一件事。
```

Bilingual (English + Traditional Chinese). Each doc readable in 2-3 minutes.

## API Key Handling

- Each example loads `GEMINI_API_KEY` from environment via `python-dotenv`
- `.env.example` shows what's needed: `GEMINI_API_KEY=your-key-here`
- `.env` is gitignored

## What This Project Is Not

- Not a library or framework
- No tests, no CI
- No multi-agent patterns (potential follow-up project)
- No streaming (kept out to maintain simplicity)
