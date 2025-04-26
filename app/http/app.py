import dotenv
from flask_migrate import Migrate
from injector import Injector, Module, Binder

from config import Config
from internal.extension.database_extension import db
from internal.extension.migrate import migrate
from internal.router import Router
from internal.server import Http
from pkg.sqlalchemy import SQLAlchemy

dotenv.load_dotenv()
config = Config()


class ExtensionModule(Module):
    def configure(self, binder: Binder):
        binder.bind(SQLAlchemy, to=db)
        binder.bind(Migrate, to=migrate)


injector = Injector([ExtensionModule])

app = Http(__name__, config=config, db=injector.get(SQLAlchemy), migrate=injector.get(Migrate),
           router=injector.get(Router))

if __name__ == "__main__":
    app.run(debug=True)
