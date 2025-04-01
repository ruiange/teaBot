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
            {"role": "system", "content": "你是一个北京老炮，说话喜欢阴阳怪气，一股子京城味~，那叫一个地道"},
            {"role": "user", "content": content},
        ],
        stream=False
    )
    return response.choices[0].message.content
