from dataclasses import dataclass

from injector import inject

from internal.service import BuiltinToolService
from pkg.response import success_json


@inject
@dataclass
class BuiltinToolHandler:
    builtin_tool_service: BuiltinToolService

    def get_builtin_tools(self):
        builtin_tools = self.builtin_tool_service.get_builtin_tools()
        return success_json(builtin_tools)

    def get_builtin_tool(self, provider_name: str, tool_name: str):
        builtin_tool = self.builtin_tool_service.get_builtin_tool(provider_name, tool_name)
        return success_json(builtin_tool)
