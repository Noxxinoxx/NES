from confluent_kafka import Consumer
from pymongo import MongoClient
import json

# Kafka Config
KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"
KAFKA_TOPICS = ["notifications.save", "notifications.send"]
KAFKA_GROUP = "mongo-consumer-group"

# Mongo Config
MONGO_URI = "mongodb://admin:Nox1234@localhost:27017/"
DB_NAME = "NNS"
COLLECTION_NAME = "events"  # your collection name

# Setup MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

# Kafka consumer configuration
consumer_conf = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "group.id": KAFKA_GROUP,
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_conf)
consumer.subscribe(KAFKA_TOPICS)

print(f"Listening for messages on topics: {KAFKA_TOPICS}...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        try:
            data = json.loads(msg.value().decode("utf-8"))
            collection.insert_one(data)
            print(f"Inserted into MongoDB: {data}")
        except json.JSONDecodeError:
            print("❌ Failed to decode JSON message")

except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    consumer.close()
