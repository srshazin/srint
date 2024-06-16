from srint.core import server
from srint.utils.logging import get_bold_blue_str
from srint.core.models import Config
class Srint:

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
        server(port=port, config=Config(
            views_path=self.views_path,
            routes= self.routes
        ))