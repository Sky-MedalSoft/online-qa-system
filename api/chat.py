import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

# 阿里云 API 配置
ALIBABA_API_URL = "https://api.aliyun.com/your_chat_api_endpoint"  # 替换为实际的阿里云 API 端点
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    async def generate_response():
        async with httpx.AsyncClient() as client:
            # 请求正文格式可根据阿里API要求更改
            data = {
                "message": request.message,
                "apiKey": API_KEY,
                "apiSecret": API_SECRET
            }

            async with client.stream("POST", ALIBABA_API_URL, json=data) as response:
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail="请求失败")

                async for line in response.aiter_lines():
                    yield line  # 流式返回

    return StreamingResponse(generate_response(), media_type="text/event-stream")
