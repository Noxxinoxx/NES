from fastapi import Request
import datetime
class ConnectionHandler:
    def __init__(self, app, categorizer):
        self.categorizer = categorizer
        self.webhooks = ['radarr', 'sonarr', 'prowlarr', 'jellyseerr']
        self.app = app
        self.route()


    def process_webhook(self, payload : dict):
        normalized_event = {
            "source": payload.get("instanceName", "unknown"),
            "event_type": payload.get("eventType", "unknown"), 
            "timestamp": datetime.date.today(),
            "raw": payload
        }
        ##save_event(normalized_event)
        print(self.categorizer.categorize(normalized_event))

        return normalized_event



    def route(self):
        for hooks in self.webhooks:
            @self.app.post("/webhook/" + hooks)
            async def sonarr_webhook(request: Request):
                payload = await request.json()
                event = self.process_webhook(payload)

                return {"status" : "ok", "event" : event}