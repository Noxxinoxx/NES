from fastapi import Request
import datetime
class ConnectionHandler:
    def __init__(self, app):
        self.source = ""
        self.webhooks = ['radarr', 'sonarr']
        self.app = app
        self.route()


    def process_webhook(self, payload : dict):
        normalized_event = {
            "source": self.source,
            "event_type": payload.get("eventType", "unknown"),
            "series_title": payload.get("series", {}).get("title", "unknown"),
            "timestamp": datetime.date.today(),
            "raw": payload
        }
        ##save_event(normalized_event)
        print(normalized_event)
        return normalized_event



    def route(self):

        for hooks in self.webhooks:
            @self.app.post("/webhook/" + hooks)
            async def sonarr_webhook(request: Request):
                payload = await request.json()
                event = self.process_webhook(payload)
                return {"status" : "ok", "event" : event}