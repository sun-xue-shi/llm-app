from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool


class DDGInput(BaseModel):
    query: str = Field(description="需要搜索的查询语句")


def duckduckgo_search(**kwargs) -> BaseTool:
    """返回DuckDuckGo搜索工具"""
    return DuckDuckGoSearchRun(
        description="一个注重隐私的搜索工具，当你需要搜索时事时可以使用该工具，工具的输入是一个查询语句",
        args_schema=DDGInput,
    )
