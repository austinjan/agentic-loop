"""
Example 05: Error Recovery
Handle tool failures gracefully — the agent detects errors and adjusts its approach.

範例 05：錯誤恢復
優雅地處理工具失敗——代理偵測錯誤並調整方法。
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
# 載入環境變數
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.1-pro-preview"
MAX_ITERATIONS = 15

SANDBOX_DIR = os.path.join(os.path.dirname(__file__), "sandbox")


# --- Tool definitions ---
# --- 工具定義 ---


def calculate(expression: str) -> str:
    """
    Evaluate a math expression. Returns an error string on failure.
    計算數學表達式。失敗時回傳錯誤字串。
    """
    try:
        allowed_names = {"__builtins__": {}}
        result = eval(expression, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def read_file(path: str) -> str:
    """
    Read a file from the sandbox. Returns an error if the file doesn't exist.
    從沙盒讀取檔案。如果檔案不存在則回傳錯誤。
    """
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
    """
    List files in a sandbox directory.
    列出沙盒目錄中的檔案。
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
                    "description": "Relative path to the file, e.g. 'hello.txt'",
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
                parts_summary.append(
                    f"function_call={p.function_call.name}({dict(p.function_call.args)})"
                )
            elif p.function_response:
                parts_summary.append(f"function_response={p.function_response.name}")
        formatted.append(f"  {{role={role!r}, parts=[{', '.join(parts_summary)}]}}")
    return "[\n" + "\n".join(formatted) + "\n]"


def run_agent(task: str):
    """
    Run the agentic loop with error recovery.
    執行帶有錯誤恢復的代理循環。
    """
    print(f"[Task] {task}")
    print("=" * 50)

    # System instruction that encourages the agent to handle errors
    # 系統指令，鼓勵代理處理錯誤
    system_instruction = """You are a helpful agent with access to tools. Use them to complete the task.

If a tool returns an error:
- Read the error message carefully
- Think about what went wrong
- Try a different approach (e.g., list the directory first to find the correct filename)
- Do NOT repeat the exact same call that failed

Always explain your reasoning before and after using tools."""

    tools = types.Tool(function_declarations=tool_declarations)
    config = types.GenerateContentConfig(
        tools=[tools],
        system_instruction=system_instruction,
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

                # Highlight errors so the learner can see the recovery in action
                # 標示錯誤，讓學習者看到錯誤恢復的過程
                if result.startswith("Error:"):
                    print(f"[Tool Error] {result}")
                else:
                    print(f"[Tool Result] {result}")

                function_response_parts.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response={"result": result},
                    )
                )

            # Observe: send results back (including errors)
            # 觀察：將結果發送回去（包括錯誤）
            contents.append(types.Content(role="user", parts=function_response_parts))

        else:
            print(f"\n[Done] {response.text}")
            return response.text

    print("\n[Warning] Max iterations reached.")
    return None


def main():
    # This task intentionally references a wrong filename
    # The agent should fail, discover the correct name, and recover
    # 這個任務故意引用了錯誤的檔名
    # 代理應該失敗、發現正確名稱並恢復
    task = (
        "Read the file called 'people.csv' from the sandbox and tell me "
        "the names of everyone listed"
    )
    run_agent(task)


if __name__ == "__main__":
    main()
