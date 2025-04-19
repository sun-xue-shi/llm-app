from dataclasses import dataclass

from flask import Flask, Blueprint
from injector import inject

from internal.handler.app_handler import AppHandler


@inject
@dataclass
class Router:
    app_handler: AppHandler

    def register_router(self, app: Flask):
        """创建一个蓝图"""
        bp = Blueprint("llm_app", __name__, url_prefix="")

        """url与控制器绑定"""
        bp.add_url_rule("/app/chat", methods=["POST"], view_func=self.app_handler.completion)
        bp.add_url_rule("/app", methods=["POST"], view_func=self.app_handler.create_app)
        bp.add_url_rule("/app/<id>", methods=["GET"], view_func=self.app_handler.get_app)
        bp.add_url_rule("/app/<id>", methods=["DELETE"], view_func=self.app_handler.del_app)
        bp.add_url_rule("/app/<id>", methods=["POST"], view_func=self.app_handler.update_app)

        """在应用上注册蓝图"""
        app.register_blueprint(bp)
