"""
Example 03: Tool Use
Give the agent a tool (calculator) and handle the tool-use protocol in the loop.

範例 03：工具使用
給代理一個工具（計算機），並在循環中處理工具使用協議。

What's new from Example 02:
- The model can REQUEST a function call (it never executes code itself)
- Your code EXECUTES the function and sends the result back
- The loop ends when the model responds with text (no function_call)

與範例 02 的差異：
- 模型可以「請求」函式呼叫（它自己從不執行程式碼）
- 你的程式碼「執行」函式，並將結果送回
- 當模型以文字回應（沒有 function_call）時，循環結束
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"
MAX_ITERATIONS = 10


# ============================================================
# STEP 1: Define your tool function
# 步驟 1：定義你的工具函式
#
# This is a regular Python function. The model will NEVER see
# this code — it only sees the schema you declare below.
# 這是一個普通的 Python 函式。模型永遠不會看到這段程式碼
# ——它只看到你在下方宣告的結構描述。
# ============================================================

def calculate(expression: str) -> str:
    """
    Evaluate a math expression and return the result as a string.
    計算數學表達式並以字串回傳結果。
    """
    try:
        allowed_names = {"__builtins__": {}}
        result = eval(expression, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


# ============================================================
# STEP 2: Declare the tool schema (FunctionDeclaration)
# 步驟 2：宣告工具結構描述（FunctionDeclaration）
#
# This tells the model:
#   - The tool's NAME (so the model can reference it)
#   - What the tool DOES (so the model knows when to use it)
#   - What ARGUMENTS it accepts (so the model can fill them in)
#
# 這告訴模型：
#   - 工具的「名稱」（讓模型可以引用它）
#   - 工具「做什麼」（讓模型知道何時使用它）
#   - 接受什麼「參數」（讓模型可以填入）
# ============================================================

calculator_declaration = types.FunctionDeclaration(
    name="calculate",
    description=(
        "Evaluate a math expression. "
        "Examples: '2 + 3', '15 * 0.15', '100 / 4'. "
        "Returns the numeric result as a string."
    ),
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


# ============================================================
# STEP 3: Create a dispatch table
# 步驟 3：建立調度表
#
# Maps tool names (strings from the API) → actual Python functions.
# When the model says "call calculate", we look up "calculate" here.
# 將工具名稱（來自 API 的字串）→ 對應到實際的 Python 函式。
# 當模型說「呼叫 calculate」時，我們在這裡查找 "calculate"。
# ============================================================

tool_functions = {
    "calculate": calculate,
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
                parts_summary.append(
                    f"function_response={p.function_response.name}"
                )
        formatted.append(
            f"  {{role={role!r}, parts=[{', '.join(parts_summary)}]}}"
        )
    return "[\n" + "\n".join(formatted) + "\n]"


# ============================================================
# STEP 4: The agentic loop with tool-use handling
# 步驟 4：帶有工具使用處理的代理循環
# ============================================================

def run_agent(task: str):
    """
    Run the agentic loop with tool use.
    執行帶有工具使用的代理循環。
    """
    print(f"[Task] {task}")
    print("=" * 60)

    # Register tool schemas with the model config
    # 將工具結構描述註冊到模型配置中
    tools = types.Tool(function_declarations=[calculator_declaration])
    config = types.GenerateContentConfig(
        tools=[tools],
        # IMPORTANT: Disable automatic function calling.
        # We want to handle tool calls ourselves in the loop,
        # so we can see exactly what's happening.
        # 重要：停用自動函式呼叫。
        # 我們想在循環中自己處理工具呼叫，這樣才能看到確切發生了什麼。
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True,
        ),
    )

    # Start the conversation with the user's task
    # 以使用者的任務開始對話
    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=task)],
        )
    ]

    for i in range(MAX_ITERATIONS):
        print(f"\n--- Iteration {i + 1} ---")

        # ── THINK: Send the conversation to the model ──
        # ── 思考：將對話送給模型 ──
        print(f"[API Request] model={MODEL}, contents={_format_contents(contents)}")
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        # ── CHECK: Did the model return a function_call or text? ──
        # ── 檢查：模型回傳的是 function_call 還是文字？ ──
        #
        # This is THE key decision point in tool use:
        #   - function_calls exist → model wants to use a tool (continue loop)
        #   - no function_calls   → model is done, returned final text (exit loop)
        #
        # 這是工具使用中「最關鍵」的判斷點：
        #   - function_calls 存在 → 模型想使用工具（繼續循環）
        #   - 沒有 function_calls → 模型完成了，回傳最終文字（結束循環）

        if not response.function_calls:
            # ── EXIT: Model responded with text — we're done ──
            # ── 結束：模型以文字回應——完成了 ──
            print(f"\n[Done] {response.text}")
            return response.text

        # ── ACT: Model requested a tool call — execute it ──
        # ── 行動：模型請求了工具呼叫——執行它 ──
        #
        # First, append the model's response to the conversation.
        # This keeps the conversation history complete:
        #   [user] → [model: function_call] → [user: function_response] → ...
        #
        # 首先，將模型的回應加入對話。
        # 這讓對話歷史保持完整：
        #   [user] → [model: function_call] → [user: function_response] → ...

        if response.candidates and response.candidates[0].content:
            contents.append(response.candidates[0].content)

        # Execute each function call the model requested.
        # (A model can request multiple tool calls in one response.)
        # 執行模型請求的每個函式呼叫。
        # （模型可以在一次回應中請求多個工具呼叫。）

        function_response_parts = []
        for fc in response.function_calls:
            tool_name = fc.name
            tool_args = dict(fc.args)
            print(f"[Tool Call] Model requested: {tool_name}({tool_args})")

            # Look up and execute the actual function
            # 查找並執行實際的函式
            func = tool_functions[tool_name]
            result = func(**tool_args)
            print(f"[Tool Result] {tool_name} returned: {result}")

            # Build the function_response to send back
            # 建構要送回的 function_response
            function_response_parts.append(
                types.Part.from_function_response(
                    name=tool_name,
                    response={"result": result},
                )
            )

        # ── OBSERVE: Send tool results back to the model ──
        # ── 觀察：將工具結果送回模型 ──
        #
        # The function_response goes in a "user" role message.
        # This completes the handshake:
        #   Model says: "call calculate('280 * 0.15')"
        #   We reply:   "calculate returned 42.0"
        #   Model then: uses the result to form its next response
        #
        # function_response 放在 "user" 角色的訊息中。
        # 這完成了握手：
        #   模型說：「呼叫 calculate('280 * 0.15')」
        #   我們回覆：「calculate 回傳了 42.0」
        #   然後模型：用結果來形成下一個回應

        contents.append(
            types.Content(role="user", parts=function_response_parts)
        )

        # Loop back to THINK — the model will see the tool result
        # and decide what to do next (call another tool, or respond with text)
        # 回到「思考」——模型會看到工具結果，
        # 然後決定下一步（呼叫另一個工具，或以文字回應）

    print("\n[Warning] Max iterations reached.")
    return None


def main():
    # A task that requires the calculator tool
    # 一個需要計算機工具的任務
    task = "What is 15% of 280, then add 42 to the result?"
    run_agent(task)


if __name__ == "__main__":
    main()
