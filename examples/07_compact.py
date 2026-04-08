"""
Example 07: Compact (Context Compaction)
When the conversation gets too long, summarize older messages to stay
within the model's context window.

範例 07：壓縮（上下文壓縮）
當對話太長時，摘要較舊的訊息以保持在模型的上下文窗口內。

What's new from Example 06:
- Token counting after each response
- Automatic compaction when approaching the token limit
- The agent keeps working seamlessly after compaction

與範例 06 的差異：
- 每次回應後計算 token 數
- 接近 token 限制時自動壓縮
- 壓縮後代理無縫繼續工作
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"
MAX_ITERATIONS = 10

SANDBOX_DIR = os.path.join(os.path.dirname(__file__), "sandbox")

# ============================================================
# Compaction settings / 壓縮設定
#
# TOKEN_LIMIT: the max tokens we allow before triggering compaction.
#   (Set low here for demo purposes — in production you'd set this
#    closer to the model's actual context window.)
# RECENT_TO_KEEP: number of recent messages to preserve as-is.
#   These are NOT summarized — they keep the agent's immediate
#   context intact.
#
# TOKEN_LIMIT：觸發壓縮前允許的最大 token 數。
#   （這裡設得較低以便示範——生產環境中你會設得接近模型的實際上下文窗口。）
# RECENT_TO_KEEP：保留不動的近期訊息數量。
#   這些不會被摘要——它們讓代理的即時上下文保持完整。
# ============================================================

TOKEN_LIMIT = 2000  # Low for demo; real usage: 100_000+
RECENT_TO_KEEP = 4  # Keep the last 4 messages untouched


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


# ============================================================
# Token counting / Token 計算
# ============================================================

def count_tokens(contents: list) -> int:
    """
    Count the total tokens in the conversation using the Gemini API.
    使用 Gemini API 計算對話中的總 token 數。
    """
    response = client.models.count_tokens(
        model=MODEL,
        contents=contents,
    )
    return response.total_tokens


# ============================================================
# COMPACTION: The core new concept in this example
# 壓縮：這個範例的核心新概念
#
# When the conversation is too long, we:
#   1. Split into OLD messages and RECENT messages
#   2. Ask the model to summarize the OLD part
#   3. Replace OLD with a single summary message
#   4. Continue with [summary] + [recent]
#
# 當對話太長時，我們：
#   1. 分割成「舊」訊息和「近期」訊息
#   2. 請模型摘要「舊」的部分
#   3. 用一條摘要訊息取代「舊」的部分
#   4. 以 [摘要] + [近期] 繼續
# ============================================================

def compact_conversation(contents: list) -> list:
    """
    Summarize older messages and return a compacted conversation.
    摘要較舊的訊息，回傳壓縮後的對話。
    """
    total = len(contents)

    # Don't compact if conversation is too short
    # 如果對話太短就不壓縮
    if total <= RECENT_TO_KEEP:
        print("[Compact] Conversation too short to compact, skipping.")
        return contents

    # Split: old messages to summarize, recent messages to keep
    # 分割：要摘要的舊訊息，要保留的近期訊息
    old_messages = contents[:total - RECENT_TO_KEEP]
    recent_messages = contents[total - RECENT_TO_KEEP:]

    print(f"[Compact] Summarizing {len(old_messages)} old messages, "
          f"keeping {len(recent_messages)} recent messages...")

    # Build a summary request: send the old messages to the model
    # and ask it to produce a concise summary
    # 建構摘要請求：將舊訊息送給模型，請它產生簡潔的摘要
    summary_contents = old_messages + [
        types.Content(
            role="user",
            parts=[types.Part(text=(
                "Please provide a concise summary of our conversation so far. "
                "Include all key facts, results, and decisions. "
                "This summary will replace the conversation history, "
                "so don't leave out anything important.\n\n"
                "請提供我們到目前為止對話的簡潔摘要。"
                "包含所有關鍵事實、結果和決定。"
                "這個摘要將取代對話歷史，所以不要遺漏任何重要內容。"
            ))],
        )
    ]

    summary_response = client.models.generate_content(
        model=MODEL,
        contents=summary_contents,
        config=types.GenerateContentConfig(),  # No tools needed for summary
    )

    summary_text = summary_response.text
    print(f"[Compact] Summary: {summary_text[:120]}...")

    # Build the compacted conversation:
    #   [1 summary message] + [recent messages]
    # 建構壓縮後的對話：
    #   [1 條摘要訊息] + [近期訊息]
    compacted = [
        types.Content(
            role="user",
            parts=[types.Part(text=(
                f"[Previous conversation summary]\n{summary_text}"
            ))],
        ),
        types.Content(
            role="model",
            parts=[types.Part(text=(
                "Understood. I have the context from our previous conversation. "
                "How can I help you next?"
            ))],
        ),
    ] + recent_messages

    old_tokens = count_tokens(contents)
    new_tokens = count_tokens(compacted)
    print(f"[Compact] Tokens: {old_tokens} → {new_tokens} "
          f"(saved {old_tokens - new_tokens})")

    return compacted


def _format_contents(contents):
    """Format the contents list for display. / 格式化 contents 以供顯示。"""
    formatted = []
    for c in contents:
        role = c.role
        parts_summary = []
        for p in c.parts:
            if p.text:
                text_preview = p.text[:80] + ("..." if len(p.text) > 80 else "")
                parts_summary.append(f"text={text_preview!r}")
            elif p.function_call:
                parts_summary.append(
                    f"function_call={p.function_call.name}({dict(p.function_call.args)})"
                )
            elif p.function_response:
                parts_summary.append(
                    f"function_response={p.function_response.name}"
                )
        formatted.append(
            f"  {{role={role!r}, parts=[{', '.join(parts_summary)}]}}"
        )
    return "[\n" + "\n".join(formatted) + "\n]"


def process_tool_calls(response, contents, config):
    """
    Handle tool calls until the model produces a text response.
    處理工具呼叫直到模型產生文字回應。
    """
    for _ in range(MAX_ITERATIONS):
        if not response.function_calls:
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

        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

    return response


def main():
    """
    Interactive chat with automatic compaction.
    帶有自動壓縮的互動式聊天。
    """
    print("Agentic Chat with Compaction (type 'quit' to exit)")
    print("帶有壓縮功能的代理聊天（輸入 'quit' 離開）")
    print(f"Token limit: {TOKEN_LIMIT} | Recent to keep: {RECENT_TO_KEEP}")
    print("=" * 60)

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
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
    )

    contents = []

    while True:
        user_input = input("\n[You] ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye! / 再見！")
            break
        if not user_input:
            continue

        contents.append(
            types.Content(
                role="user",
                parts=[types.Part(text=user_input)],
            )
        )

        print(f"[API Request] model={MODEL}, contents={_format_contents(contents)}")
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        response = process_tool_calls(response, contents, config)

        contents.append(response.candidates[0].content)

        print(f"\n[Agent] {response.text}")

        # ── CHECK: Should we compact? ──
        # ── 檢查：是否應該壓縮？──
        #
        # After each turn, count the tokens in the conversation.
        # If we're over the limit, compact before the next turn.
        # 每次輪次後，計算對話中的 token 數。
        # 如果超過限制，在下一輪之前壓縮。
        token_count = count_tokens(contents)
        print(f"\n[Tokens] {token_count} / {TOKEN_LIMIT}")

        if token_count > TOKEN_LIMIT:
            print(f"[Tokens] Limit exceeded! Compacting conversation...")
            contents = compact_conversation(contents)


if __name__ == "__main__":
    main()
