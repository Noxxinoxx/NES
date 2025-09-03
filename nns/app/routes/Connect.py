from fastapi import Request
import datetime

from common.kafka_sender import Sender


class ConnectionHandler:
    def __init__(self, app, categorizer):
        self.categorizer = categorizer
        self.kafka = Sender()
        self.webhooks = ['radarr', 'sonarr', 'prowlarr', 'jellyseerr']
        self.app = app
        self.route()


    def process_webhook(self, payload : dict):
        normalized_event = {
            "source": payload.get("instanceName", "unknown"),
            "event_type": payload.get("eventType", "unknown"), 
            "timestamp": datetime.date.today().isoformat(),
            "raw": payload
        }
        #save_event(normalized_event)
        categorized_data = self.categorizer.categorize(normalized_event)
        #send event to kafka.

        self.kafka.send(categorized_data)
        
        return {"status" : 200}



    def route(self):
        for hooks in self.webhooks:
            @self.app.post("/webhook/" + hooks)
            async def sonarr_webhook(request: Request):
                payload = await request.json()
                event = self.process_webhook(payload)
                return {"status" : "ok", "event" : event}