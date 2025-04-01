import os
from dotenv import load_dotenv  # 新增导入
# 加载 .env 文件
load_dotenv()
import logging


# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

api_key = os.getenv("API_KEY")  # 从环境变量中获取 API_KEY
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")
def ai_reply(content):
    logging.info(f"api_key:${api_key}")
    client = OpenAI(api_key=api_key, base_url=base_url)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你现在身处的环境是一个微信群；你是一个摩托车爱好者，你的座驾是雅马哈；精通摩托车，可以帮助群友解答摩托车问题"},
            {"role": "user", "content": content},
        ],
        stream=False
    )
    return response.choices[0].message.content
