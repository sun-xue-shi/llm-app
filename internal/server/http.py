from flask import Flask

from config import Config
from internal.router import Router


class Http(Flask):
    def __init__(self, *args, config: Config, router: Router, **kwargs):
        super().__init__(*args, **kwargs)

        router.register_router(self)

        self.config.from_object(config)
