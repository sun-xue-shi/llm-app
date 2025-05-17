from dataclasses import dataclass

from flask import Flask, Blueprint
from injector import inject

from internal.handler import BuiltinToolHandler
from internal.handler.api_tool import ApiToolHandler
from internal.handler.app_handler import AppHandler


@inject
@dataclass
class Router:
    app_handler: AppHandler
    builtin_tool_handler: BuiltinToolHandler
    api_tool_handler: ApiToolHandler

    def register_router(self, app: Flask):
        """创建一个蓝图"""
        bp = Blueprint("llm_app", __name__, url_prefix="")

        """url与控制器绑定"""
        bp.add_url_rule("/app/chat", methods=["POST"], view_func=self.app_handler.completion)
        bp.add_url_rule("/app", methods=["POST"], view_func=self.app_handler.create_app)
        bp.add_url_rule("/app/<id>", methods=["GET"], view_func=self.app_handler.get_app)
        bp.add_url_rule("/app/<id>", methods=["DELETE"], view_func=self.app_handler.del_app)
        bp.add_url_rule("/app/<id>", methods=["POST"], view_func=self.app_handler.update_app)

        # 内置插件工具模块
        bp.add_url_rule("/builtin_tools", methods=["GET"], view_func=self.builtin_tool_handler.get_builtin_tools)
        bp.add_url_rule(
            "/builtin_tools/<provider_name>/tools/<tool_name>", methods=["GET"],
            view_func=self.builtin_tool_handler.get_builtin_tool
        )
        bp.add_url_rule(
            "/builtin_tools/<provider_name>/icon", methods=["GET"],
            view_func=self.builtin_tool_handler.get_provider_icon
        )
        bp.add_url_rule(
            "/builtin_tools/categories", methods=["GET"],
            view_func=self.builtin_tool_handler.get_categories
        )
        bp.add_url_rule("/api_tools/validate_openapi_schema", methods=["POST"],
                        view_func=self.api_tool_handler.vaildate_openapi_schema)
        bp.add_url_rule("/api_tools", methods=["POST"], view_func=self.api_tool_handler.create_api_tool_provider)
        bp.add_url_rule("/api_tools/<provider_id>", methods=["GET"],
                        view_func=self.api_tool_handler.get_api_tool_provider)
        bp.add_url_rule("/api_tools/<provider_id>/tools/<tool_name>", methods=["GET"],
                        view_func=self.api_tool_handler.get_api_tool)
        bp.add_url_rule(
            "/api-tools/<uuid:provider_id>/delete",
            methods=["POST"],
            view_func=self.api_tool_handler.delete_api_tool_provider,
        )
        bp.add_url_rule("/api_tools", methods=["GET"], view_func=self.api_tool_handler.get_api_tool_providers_with_page)

        """在应用上注册蓝图"""
        app.register_blueprint(bp)
