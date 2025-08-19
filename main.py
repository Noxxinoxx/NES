from fastapi import FastAPI, Request
from NNS.Connections.Connect import ConnectionHandler

app = FastAPI()


class RouteHandler:
    def __init__(self):
        self.app = app
        self.sonarr = ConnectionHandler(self.app)

router = RouteHandler()