import uuid
from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy
from injector import inject

from internal.model import App


@inject
@dataclass
class AppService:
    db: SQLAlchemy

    def create_app(self) -> App:
        app = App(name="test", icon="", description="test_desc", account_id=uuid.uuid4())

        self.db.session.add(app)
        self.db.session.commit()
        return app

    def get_app(self, id: uuid.uuid4()) -> App:
        return self.db.session.query(App).get(id)

    def del_app(self, id: uuid.uuid4()) -> App:
        app = self.get_app(id)
        self.db.session.delete(app)
        self.db.session.commit()
        return app

    def update_app(self, id: uuid.uuid4()) -> App:
        app = self.get_app(id)
        app.name = "test_update"
        self.db.session.commit()
        return app
