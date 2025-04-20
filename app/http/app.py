import dotenv
from injector import Injector, Module, Binder

from config import Config
from internal.extension.database_extension import db
from internal.router import Router
from internal.server import Http
from pkg.sqlalchemy import SQLAlchemy

dotenv.load_dotenv()
config = Config()


class ExtensionModule(Module):
    def configure(self, binder: Binder):
        binder.bind(SQLAlchemy, to=db)


injector = Injector([ExtensionModule])

app = Http(__name__, config=config, db=injector.get(SQLAlchemy), router=injector.get(Router))

if __name__ == "__main__":
    app.run(debug=True)
