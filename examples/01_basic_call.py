"""
Example 01: Basic Call
Send a single prompt to Gemini and print the response.

範例 01：基本呼叫
發送一個提示給 Gemini 並印出回應。
"""

import os

from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
# 從 .env 檔案載入環境變數
load_dotenv()

# Create a Gemini client with your API key
# 使用你的 API 金鑰建立 Gemini 客戶端
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# The model to use for generation
# 用於生成的模型
MODEL = "gemini-3.1-flash-lite-preview"


def main():
    # Define a simple prompt
    # 定義一個簡單的提示
    prompt = "Explain what an AI agent is in 3 sentences."

    print(f"[Prompt] {prompt}")
    print("-" * 40)

    # Show the actual API payload
    # 顯示實際發送的 API 內容
    print(f"[API Request] model={MODEL}, contents={prompt!r}")

    # Send the prompt to Gemini and get the response
    # 發送提示給 Gemini 並取得回應
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    # Print the response text
    # 印出回應文字
    print(f"[Response] {response.text}")


if __name__ == "__main__":
    main()
