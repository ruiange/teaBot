

# webapi.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# 创建 FastAPI 应用实例
app = FastAPI()

# 定义请求体的模型
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# 定义 POST 接口
@app.post("/")
async def create_item(item: Item):
    print("Received JSON data:", item.dict())
    # 这里可以处理接收到的 JSON 数据
    return {"message": "Item received", "item": item.dict()}