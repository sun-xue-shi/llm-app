from flask import Flask

from config import Config
from internal.exception import CustomException
from internal.model import App
from internal.router import Router
from pkg.response import Response, json, HttpCode
from pkg.sqlalchemy import SQLAlchemy


class Http(Flask):
    def __init__(self, *args, config: Config, db: SQLAlchemy, router: Router, **kwargs):
        super().__init__(*args, **kwargs)

        router.register_router(self)

        self.config.from_object(config)

        db.init_app(self)
        with self.app_context():
            _ = App()
            db.create_all()

        self.register_error_handler(Exception, self._register_error_handler)

    def _register_error_handler(self, error: Exception):
        print("error", error)
        if isinstance(error, CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if error.data is not None else {}
            ))
        return json(Response(
            code=HttpCode.FAIL,
            message=str(error),
            data={}
        ))
