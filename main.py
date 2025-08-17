from fastapi import FastAPI, Request
from Connections.sonarr import SonarrHandler

app = FastAPI()


class RouteHandler:
    def __init__(self):
        self.app = app
        self.sonarr = SonarrHandler(self.app)

router = RouteHandler()