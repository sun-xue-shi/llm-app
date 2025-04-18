from dataclasses import dataclass

from injector import inject
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from internal.schema.app_schema import CompletionReq
from pkg.response import success_json, valid_error_json


@inject
@dataclass
class AppHandler:
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
