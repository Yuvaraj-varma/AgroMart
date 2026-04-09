from kafka import KafkaProducer
import json
import os

# Kafka configuration
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_ORDER_TOPIC", "order-topic")

# Initialize Kafka producer lazily (won't crash if Kafka is not running)
producer = None

def get_producer():
    global producer
    if producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BOOTSTRAP],
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                linger_ms=5
            )
            print("✅ Kafka producer connected")
        except Exception as e:
            print(f"⚠️ Kafka not available: {e}")
            producer = None
    return producer

def send_order_to_kafka(order_data: dict):
    p = get_producer()
    if p is None:
        print(f"⚠️ Kafka unavailable — order saved locally: {order_data}")
        return
    p.send(KAFKA_TOPIC, value=order_data)
    p.flush()
    print(f"✅ Sent to Kafka: {order_data}")
