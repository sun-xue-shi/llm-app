from langchain_community.tools.wikipedia.tool import WikipediaQueryRun, WikipediaQueryInput
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import BaseTool

from internal.lib import add_attribute


@add_attribute("args_schema", WikipediaQueryInput)
def wikipedia_search(**kwargs) -> BaseTool:
    """返回维基百科搜索工具"""
    return WikipediaQueryRun(
        api_wrapper=WikipediaAPIWrapper(),
    )
