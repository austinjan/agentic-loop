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
                parts_summary.append(f"function_call={p.function_call.name}({dict(p.function_call.args)})")
            elif p.function_response:
                parts_summary.append(f"function_response={p.function_response.name}")
        formatted.append(f"  {{role={role!r}, parts=[{', '.join(parts_summary)}]}}")
    return "[\n" + "\n".join(formatted) + "\n]"


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
        print(f"  [API Request] model={MODEL}, contents={_format_contents(contents)}")
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
        print(f"[API Request] model={MODEL}, contents={_format_contents(contents)}")
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
