from fastapi import FastAPI
from Connections.Connect import ConnectionHandler
from Helpers.categorizer import Categorizer

app = FastAPI()
categoriser = Categorizer("./config.json")

class RouteHandler:
    def __init__(self):
        self.app = app
        self.handler = ConnectionHandler(self.app, categoriser)

router = RouteHandler()