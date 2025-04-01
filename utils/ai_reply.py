import os
from dotenv import load_dotenv  # 新增导入

# 加载 .env 文件
load_dotenv()

# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

def ai_reply(content):
    api_key = os.getenv("API_KEY")  # 从环境变量中获取 API_KEY
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": content},
        ],
        stream=False
    )
    return response.choices[0].message.content
