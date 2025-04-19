import uuid
from dataclasses import dataclass

from injector import inject
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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

        print("query: ", req.query.data)

        prompt = ChatPromptTemplate.from_template("{query}")
        llm = ChatOpenAI(model="deepseek-chat")
        parser = StrOutputParser()

        chain = prompt | llm | parser

        content = chain.invoke({"query": req.query.data})

        return success_json({"content": content})
