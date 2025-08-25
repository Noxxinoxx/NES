from fastapi import Request
import datetime

from Helpers.send_mail import sender

class ConnectionHandler:
    def __init__(self, app, categorizer):
        self.categorizer = categorizer
        self.sender = sender("nox@noxi.pro")
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
        #save_event(normalized_event)
        categorized_data = self.categorizer.categorize(normalized_event)



        self.sender.set_email_info(categorized_data)    
        self.sender.send_email_with_info()
        return normalized_event



    def route(self):
        for hooks in self.webhooks:
            @self.app.post("/webhook/" + hooks)
            async def sonarr_webhook(request: Request):
                payload = await request.json()
                event = self.process_webhook(payload)
                return {"status" : "ok", "event" : event}