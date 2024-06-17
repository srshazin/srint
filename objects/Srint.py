from srint.core import server
from srint.utils.logging import get_bold_blue_str
from srint.core.models import Config
from srint.utils.logging import perror
from srint.core.context import ContextManager

class Srint:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Srint, cls).__new__(cls, *args, **kwargs)
            return cls._instance
        else:
            perror("Srint() can be initialized only once throughout the application")
    def __init__(self):
        print(get_bold_blue_str("Welcome to srint micro-server"))


    views_path: str = "views"
    routes = []

    def add_route(self, path: str,  handler):
        if path.startswith("/"):
            self.routes.append({
                "path": path,
                "handler": handler
            })
        else:
            raise ValueError("routes paths must start with /")

    def serve(self, port: int= 6942):
        app_conf = Config(
            views_path=self.views_path,
            routes= self.routes,
            port=port,
            host="0.0.0.0"
        )
        ContextManager.set_config(app_conf)
        server(port=port, config=app_conf)