from confluent_kafka import Producer
import json

class Sender:
    def __init__(self):
        self.conf = {"bootstrap.servers" : "localhost:29092"}
        self.topic_send = "notifications.send"
        self.topic_save = "notifications.save"
        self.producer = Producer(self.conf)
        

    def delivery_report(self, err, message):
        if err:
            print(f"Delivery failed: {err}")
        else:
            print(f"Message delivered to {message.topic()} [{message.partition()}]")

    def send(self,json_data):       
        #send the kafka event to tells that we both want to save and send to notification.
        self.producer.produce(self.topic_save, value=json.dumps(json_data), callback=self.delivery_report) 
        self.producer.flush()
        self.producer.produce(self.topic_send, value=json.dumps(json_data), callback=self.delivery_report)
        self.producer.flush()
