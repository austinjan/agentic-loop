"""
Example 02: Simple Loop
The core agentic loop — Think, Decide, Repeat — without any tools.

範例 02：簡單循環
核心代理循環——思考、決定、重複——不使用任何工具。
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
# 從 .env 檔案載入環境變數
load_dotenv()

# Create a Gemini client
# 建立 Gemini 客戶端
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"

# Maximum number of loop iterations to prevent infinite loops
# 最大循環次數，防止無限循環
MAX_ITERATIONS = 10


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
    Run the agentic loop for a given task.
    對給定任務執行代理循環。
    """
    print(f"[Task] {task}")
    print("=" * 50)

    # System instruction that tells the model how to behave as an agent
    # 系統指令，告訴模型如何作為代理運作
    system_instruction = """You are a step-by-step reasoning agent. Break down the task and think through it step by step.

For each step:
1. State what you're thinking about
2. Provide your reasoning
3. State your conclusion for this step

When you have reached the final answer, start your response with "FINAL ANSWER:" followed by your complete answer.

Do not output "FINAL ANSWER:" until you are fully done reasoning."""

    # Build the conversation history
    # 建構對話歷史
    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=task)],
        )
    ]

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
    )

    for i in range(MAX_ITERATIONS):
        print(f"\n--- Iteration {i + 1} ---")

        # Think: ask the model to reason about the current state
        # 思考：請模型對目前狀態進行推理
        print(f"[API Request] model={MODEL}, contents={_format_contents(contents)}")
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        response_text = response.text
        print(f"[Response]\n{response_text}")

        # Decide: check if the model has reached a final answer
        # 決定：檢查模型是否已達到最終答案
        if "FINAL ANSWER:" in response_text:
            print("\n" + "=" * 50)
            print("[Done] Agent has reached a final answer.")
            final_answer = response_text.split("FINAL ANSWER:")[-1].strip()
            print(f"[Final Answer] {final_answer}")
            return final_answer

        # Append model response and prompt it to continue
        # 加入模型回應並提示它繼續
        contents.append(response.candidates[0].content)
        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        text="Continue your reasoning. If you have reached the final answer, start with 'FINAL ANSWER:'"
                    )
                ],
            )
        )

    print("\n[Warning] Max iterations reached without a final answer.")
    print("警告：已達最大循環次數，但未得到最終答案。")
    return None


def main():
    # A task that requires multi-step reasoning
    # 一個需要多步驟推理的任務
    task = "畫一個三角形輸出的範例，提供 source code"
    run_agent(task)


if __name__ == "__main__":
    main()
