from kafka import KafkaProducer
import json
from app.core.config import settings

producer = None

def get_producer():
    global producer
    if producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=[settings.KAFKA_BOOTSTRAP],
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
        print(f"⚠️ Kafka unavailable — order not sent: {order_data}")
        return
    p.send(settings.KAFKA_ORDER_TOPIC, value=order_data)
    p.flush()
    print(f"✅ Sent to Kafka: {order_data}")
