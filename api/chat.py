import os

from fastapi import APIRouter, HTTPException
from openai import OpenAI
from sse_starlette.sse import EventSourceResponse

chatR = APIRouter()

# 设置API密钥
os.environ['DASHSCOPE_API_KEY'] = '密钥'

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


@chatR.get("/chat")
async def chat(query: str):
    async def generate():
        try:
            response = client.chat.completions.create(
                model="qwen-turbo",
                messages=[
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': query}
                ],
                temperature=0.8,
                stream=True
            )
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                for char in content:  # 逐字输出
                    yield char
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return EventSourceResponse(generate())
