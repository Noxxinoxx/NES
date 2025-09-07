from confluent_kafka import Producer
import json
#1
class Sender:
    def __init__(self):
        self.public_conf = {"bootstrap.servers" : "localhost:29092"}
        self.conf = {"bootstrap.servers" : "kafka:9092"}
        self.topic_send = "notifications.send"
        self.topic_save = "notifications.save"
        self.topic_alert = "alerts"
        self.producer = Producer(self.conf)
        self.producer_public = Producer(self.public_conf)
        

    def delivery_report(self, err, message):
        if err:
            print(f"Delivery failed: {err}")
        else:
            print(f"Message delivered to {message.topic()} [{message.partition()}]")

    def send(self,json_data):       
        #send the kafka event to tells that we both want to save and send to notification.
        self.producer.produce(self.topic_send, value=json.dumps(json_data), callback=self.delivery_report) 
        self.producer.flush()

    def save(self, json_data):
        self.producer.produce(self.topic_save, value=json.dumps(json_data), callback=self.delivery_report) 
        self.producer.flush()

    def send_alert(self, json_data):
        self.producer_public.produce(self.topic_alert, value=json.dumps(json_data), callback=self.delivery_report)
        self.producer_public.flush()