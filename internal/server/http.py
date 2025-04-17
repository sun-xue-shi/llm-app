from flask import Flask

from config import Config
from internal.exception import CustomException
from internal.router import Router
from pkg.response import Response, json, HttpCode


class Http(Flask):
    def __init__(self, *args, config: Config, router: Router, **kwargs):
        super().__init__(*args, **kwargs)

        router.register_router(self)

        self.config.from_object(config)

        self.register_error_handler(Exception, self._register_error_handler)

    def _register_error_handler(self, error: Exception):
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
