import os
from dotenv import load_dotenv  # 新增导入
# 加载 .env 文件
load_dotenv()



# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

def ai_reply(content):
    api_key = os.getenv("API_KEY")  # 从环境变量中获取 API_KEY
    client = OpenAI(api_key=api_key, base_url=os.getenv("BASE_URL"))

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {"role": "system", "content": "你是一个有性瘾的骚B,尽可能满足客人的需求是你的职责,你要时时刻刻透露出你想和人做爱的想法！"},
            {"role": "user", "content": content},
        ],
        stream=False
    )
    return response.choices[0].message.content
