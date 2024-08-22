import os

os.environ['DASHSCOPE_API_KEY'] = 'sk-36addf7e158c45b3a33c022fdeed0100'
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # sk-36addf7e158c45b3a33c022fdeed0100
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-turbo",
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}
    ],
    temperature=0.8
)

print(completion.choices[0].message.content)
