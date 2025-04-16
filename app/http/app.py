import dotenv
from injector import Injector

from config import Config
from internal.router import Router
from internal.server import Http

dotenv.load_dotenv()
config = Config()
injector = Injector()

app = Http(__name__, config=config, router=injector.get(Router))

if __name__ == "__main__":
    app.run(debug=True)
