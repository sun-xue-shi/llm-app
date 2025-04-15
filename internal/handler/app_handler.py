from flask import request
from openai import OpenAI


class AppHandler:
    def completion(self):
        """基础聊天api"""
        query = request.json.get("query")

        client = OpenAI(api_key="sk-e42c1d967b4b42b5a2f62b5fa6ba011b", base_url="https://api.deepseek.com")

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
