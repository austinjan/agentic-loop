"""
Example 04: Multi Tool
Multiple tools (calculator + filesystem) with multi-step reasoning.

範例 04：多工具
多個工具（計算機 + 檔案系統）與多步驟推理。
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
MAX_ITERATIONS = 15

# Sandbox directory for filesystem tools — restrict access to this folder
# 檔案系統工具的沙盒目錄——限制只能存取此資料夾
SANDBOX_DIR = os.path.join(os.path.dirname(__file__), "sandbox")


# --- Tool definitions ---
# --- 工具定義 ---

def calculate(expression: str) -> str:
    """
    Evaluate a math expression and return the result.
    計算數學表達式並回傳結果。
    """
    try:
        allowed_names = {"__builtins__": {}}
        result = eval(expression, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def read_file(path: str) -> str:
    """
    Read and return the contents of a file in the sandbox directory.
    讀取並回傳沙盒目錄中檔案的內容。
    """
    # Resolve to absolute path within sandbox
    # 解析為沙盒內的絕對路徑
    full_path = os.path.normpath(os.path.join(SANDBOX_DIR, path))

    # Security check: ensure the path is inside the sandbox
    # 安全檢查：確保路徑在沙盒內
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
    """
    List files and folders in a directory within the sandbox.
    列出沙盒內目錄中的檔案和資料夾。
    """
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


# Tool schemas for Gemini
# Gemini 的工具結構描述
tool_declarations = [
    {
        "name": "calculate",
        "description": "Evaluate a math expression. Examples: '2 + 3', '15 * 0.15', '100 / 4'.",
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
        "description": "Read the contents of a file. The path is relative to the sandbox directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the file, e.g. 'hello.txt' or 'data.csv'",
                },
            },
            "required": ["path"],
        },
    },
    {
        "name": "list_directory",
        "description": "List files and folders in a directory. The path is relative to the sandbox directory. Use '.' for the root sandbox directory.",
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

# Map of tool names to their implementations
# 工具名稱對應到實作的映射
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


def run_agent(task: str):
    """
    Run the agentic loop with multiple tools.
    執行帶有多個工具的代理循環。
    """
    print(f"[Task] {task}")
    print("=" * 50)

    tools = types.Tool(function_declarations=tool_declarations)
    config = types.GenerateContentConfig(
        tools=[tools],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=task)],
        )
    ]

    for i in range(MAX_ITERATIONS):
        print(f"\n--- Iteration {i + 1} ---")

        # Think: send conversation to Gemini
        # 思考：將對話發送給 Gemini
        print(f"[API Request] model={MODEL}, contents={_format_contents(contents)}")
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        if response.function_calls:
            contents.append(response.candidates[0].content)

            function_response_parts = []
            for fc in response.function_calls:
                print(f"[Tool Call] {fc.name}({dict(fc.args)})")

                # Act: execute the tool
                # 行動：執行工具
                func = tool_functions[fc.name]
                result = func(**fc.args)
                print(f"[Tool Result] {result}")

                function_response_parts.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response={"result": result},
                    )
                )

            # Observe: send results back
            # 觀察：將結果發送回去
            contents.append(
                types.Content(role="user", parts=function_response_parts)
            )

        else:
            print(f"\n[Done] {response.text}")
            return response.text

    print("\n[Warning] Max iterations reached.")
    return None


def main():
    # A task that requires both filesystem and calculator tools
    # 一個同時需要檔案系統和計算機工具的任務
    task = (
        "Look at the files in the sandbox directory. "
        "Read the data.csv file and calculate the average age of all people listed."
    )
    run_agent(task)


if __name__ == "__main__":
    main()
