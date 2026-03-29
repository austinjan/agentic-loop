# Agentic Loop

Learn how agentic loops work through simple, clear examples.

## What is an Agentic Loop?

An agentic loop is the core execution cycle that powers AI agents. Instead of a single prompt-and-response, the agent operates in a loop:

```
User Task
   |
   v
+-----------+
|   Think   | <---+
+-----------+     |
   |              |
   v              |
+-----------+     |
|    Act    |     |
+-----------+     |
   |              |
   v              |
+-----------+     |
|  Observe  | ----+
+-----------+
   |
   (done?)
   |
   v
 Result
```

1. **Think** — The LLM reasons about the current state and decides what to do next.
2. **Act** — The agent executes a tool call (run code, search the web, read a file, etc.).
3. **Observe** — The agent reads the result of the action.
4. **Repeat** — Loop back to Think until the task is complete.

This loop allows an AI agent to break down complex tasks, use tools, handle errors, and iteratively work toward a goal — much like a human developer would.

## Why Does This Matter?

A single LLM call can answer a question. An agentic loop can **solve a problem**. The difference:

| Single LLM Call | Agentic Loop |
|---|---|
| One-shot response | Multi-step reasoning |
| No tool use | Can call tools |
| No error recovery | Can retry and adapt |
| Limited by one prompt | Builds on prior steps |

## Project Structure

This project provides minimal, easy-to-follow examples that demonstrate the agentic loop pattern. Each example is self-contained and focuses on one concept at a time.

## Getting Started

```bash
git clone https://github.com/your-username/agentic-loop.git
cd agentic-loop
```

Explore the examples to see how agentic loops are built from scratch.

## License

MIT
