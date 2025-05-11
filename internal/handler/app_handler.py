import uuid
from dataclasses import dataclass
from operator import itemgetter
from typing import Any, Dict

from injector import inject
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.memory import BaseMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig
from langchain_core.tracers import Run
from langchain_openai import ChatOpenAI

from internal.core.tools.builtin_tools.providers import BuiltinProviderManager
from internal.schema.app_schema import CompletionReq
from internal.service import AppService, VectorDatabaseService
from pkg.response import success_json, valid_error_json, success_message


@inject
@dataclass
class AppHandler:
    app_service: AppService
    vector_database_service: VectorDatabaseService
    provider_manager: BuiltinProviderManager

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

    @classmethod
    def _load_memory_variables(cls, input: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        configurable = config.get("configurable", {})
        config_memory = configurable.get("memory", None)
        if config_memory is not None and isinstance(config_memory, BaseMemory):
            return config_memory.load_memory_variables(input)
        return {"history": []}

    @classmethod
    def _save_context(cls, run_obj: Run, config: RunnableConfig) -> None:
        configurable = config.get("configurable", {})
        config_memory = configurable.get("memory", None)
        if config_memory is not None and isinstance(config_memory, BaseMemory):
            config_memory.save_context(run_obj.inputs, run_obj.outputs)

    def completion(self):
        """基础聊天api"""

        req = CompletionReq()
        if not req.validate():
            return valid_error_json(req.errors)

        system_prompt = "你是一个强大的聊天ai，请根据对应的上下文和历史对话信息回答用户问题. \n\n <context>{context}</context>"
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
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

        retriever = self.vector_database_service.get_retriever() | self.vector_database_service.combine_documents

        chain = (RunnablePassthrough.assign(
            history=RunnableLambda(self._load_memory_variables) | itemgetter("history"),
            context=itemgetter("query") | retriever
        ) | prompt | llm | StrOutputParser()).with_listeners(on_end=self._save_context)

        content = chain.invoke({"query": req.query.data}, config={"configurable": {"memory": memory}})

        return success_json({"content": content})
