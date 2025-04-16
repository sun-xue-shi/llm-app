import os

from flask import request
from openai import OpenAI

from internal.schema.app_schema import CompletionReq


class AppHandler:
    def completion(self):
        """基础聊天api"""

        req = CompletionReq()
        if not req.validate():
            return req.errors
        query = request.json.get("query")

        """这里会自动读取环境变量的api-key"""
        client = OpenAI(base_url=os.getenv("DEEPSEEK_BASE_URL"))

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个聊天机器人，请根据用户回复输入信息"},
                {"role": "user", "content": query},
            ],
            stream=False
        )

        content = response.choices[0].message.content

        return content
