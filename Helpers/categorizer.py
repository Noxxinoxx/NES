##
## This code will handle all the notifications
## That are comming in and catagorse them
## 3 diffrent catagoise 
## 1 : important will send a stress notification
## 2 : info will also send notification
## 3 : will be stored but no notification will be sent
## 

import json

class Categorizer: 
    def __init__(self, config_path):
        # Load the config from the given path
        with open(config_path, 'r') as f:
            self.config = json.load(f)

    def categorize(self, notification_data):
        """
        notification_data example:
        {
            "service": "Radarr",
            "event": "OnMovieAdded"
        }
        """
        service_name = notification_data.get("source")
        event = notification_data.get("event_type")

        # Find matching service in config
        importance_list = self.config.get("importance", [])
        for service in importance_list:
            if service["name"] == service_name:
                # Check critical
                if event in service.get("importance_critical", []):
                    return {"category": 1, "level": "critical", "event" : event, "source" : service_name,"raw" : notification_data}
                # Check high
                if event in service.get("importance_high", []):
                    return {"category": 2, "level": "high", "event" : event ,"source" : service_name,"raw" : notification_data}
                # Check low
                if "*" in service.get("importance_low", []) or event in service.get("importance_low", []):
                    return {"category": 3, "level": "low", "event" : event,  "source" : service_name, "raw" : notification_data}

        # Default if service not found or event not matched
        return {"category": 3, "level": "low", "event" : event,  "source" : service_name, "raw" : notification_data}  # store silently