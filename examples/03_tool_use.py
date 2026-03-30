"""
Example 03: Tool Use
Add a calculator tool that the agent can call during its reasoning loop.

範例 03：工具使用
加入一個計算機工具，讓代理在推理循環中呼叫。
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


# --- Tool definitions ---
# --- 工具定義 ---

def calculate(expression: str) -> str:
    """
    Evaluate a math expression and return the result.
    計算數學表達式並回傳結果。
    """
    try:
        # Only allow safe math operations
        # 只允許安全的數學運算
        allowed_names = {"__builtins__": {}}
        result = eval(expression, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


# Define the tool schema for Gemini
# 為 Gemini 定義工具結構描述
calculator_declaration = types.FunctionDeclaration(
    name="calculate",
    description="Evaluate a math expression. Examples: '2 + 3', '15 * 0.15', '100 / 4'. Returns the numeric result.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "expression": types.Schema(
                type=types.Type.STRING,
                description="The math expression to evaluate, e.g. '2 + 3 * 4'",
            ),
        },
        required=["expression"],
    ),
)


# Map of tool names to their implementations
# 工具名稱對應到實作的映射
tool_functions = {
    "calculate": calculate,
}


def run_agent(task: str):
    """
    Run the agentic loop with tool use.
    執行帶有工具使用的代理循環。
    """
    print(f"[Task] {task}")
    print("=" * 50)

    # Configure tools for the model
    # 為模型配置工具
    tools = types.Tool(function_declarations=[calculator_declaration])
    config = types.GenerateContentConfig(
        tools=[tools],
        # Disable automatic function calling so we control the loop
        # 停用自動函式呼叫，讓我們控制循環
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True,
        ),
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
        print("[Think] Asking Gemini...")
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        # Check if the model wants to call a tool
        # 檢查模型是否想要呼叫工具
        if response.function_calls:
            # Append the model's response (contains the function call)
            # 加入模型的回應（包含函式呼叫）
            if response.candidates and response.candidates[0].content:
                contents.append(response.candidates[0].content)

            # Process each function call
            # 處理每個函式呼叫
            function_response_parts = []
            for fc in response.function_calls:
                print(f"[Tool Call] {fc.name}({dict(fc.args)})")

                # Act: execute the tool
                # 行動：執行工具
                func = tool_functions[fc.name]
                result = func(**fc.args)
                print(f"[Tool Result] {result}")

                # Build the function response
                # 建構函式回應
                function_response_parts.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response={"result": result},
                    )
                )

            # Observe: send the tool results back to Gemini
            # 觀察：將工具結果發送回 Gemini
            contents.append(
                types.Content(role="user", parts=function_response_parts)
            )

        else:
            # No tool call — the model has produced a final text response
            # 沒有工具呼叫——模型已產生最終文字回應
            print(f"\n[Done] {response.text}")
            return response.text

    print("\n[Warning] Max iterations reached.")
    return None


def main():
    task = "What is 15% of 280, then add 42 to the result?"
    run_agent(task)


if __name__ == "__main__":
    main()
