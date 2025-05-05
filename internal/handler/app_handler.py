import uuid
from dataclasses import dataclass
from operator import itemgetter

from injector import inject
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, valid_error_json, success_message


@inject
@dataclass
class AppHandler:
    app_service: AppService

    def create_app(self):
        """创建应用"""
        app = self.app_service.create_app()
        return success_message(f"创建应用成功, app_id: {app.id}")

    def get_app(self, id: uuid.uuid4()):
        """获取应用"""
        app = self.app_service.get_app(id)
        return success_message(f"获取应用成功, app_name: {app.name}")

    def del_app(self, id: uuid.uuid4()):
        """删除应用"""
        app = self.app_service.del_app(id)
        return success_message(f"删除应用成功, app_name: {app.name}")

    def update_app(self, id: uuid.uuid4()):
        """更新应用"""
        app = self.app_service.update_app(id)
        return success_message(f"更新应用成功, app_name: {app.name}")

    def completion(self):
        """基础聊天api"""

        req = CompletionReq()
        if not req.validate():
            return valid_error_json(req.errors)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个智能助手，请根据用户的问题给出回答"),
            MessagesPlaceholder("history"),
            ("human", "{query}"),
        ])

        memory = ConversationBufferWindowMemory(
            k=3,
            input_key="query",
            output_key="output",
            return_messages=True,
            chat_memory=FileChatMessageHistory(".\storage\memory\chat_history.txt")
        )

        llm = ChatOpenAI(model="deepseek-chat")

        chain = RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        ) | prompt | llm | StrOutputParser()

        content = chain.invoke({"query": req.query.data})

        memory.save_context({"query": req.query.data}, {"output": content})

        return success_json({"content": content})
