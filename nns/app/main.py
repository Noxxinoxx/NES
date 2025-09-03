from fastapi import FastAPI
from nns.app.routes.Connect import ConnectionHandler
from nns.app.services.categorizer import Categorizer
from pathlib import Path

config_path = Path(__file__).resolve().parent.parent / "config.json"


app = FastAPI()
categoriser = Categorizer(config_path)

class RouteHandler:
    def __init__(self):
        self.app = app
        self.handler = ConnectionHandler(self.app, categoriser)

router = RouteHandler()