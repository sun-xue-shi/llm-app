import io
from dataclasses import dataclass

from flask import send_file
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

    def get_provider_icon(self, provider_name: str):
        icon, mimetype = self.builtin_tool_service.get_provider_icon(provider_name)
        return send_file(io.BytesIO(icon), mimetype=mimetype)

    def get_categories(self):
        categories = self.builtin_tool_service.get_categories()
        return success_json(categories)
