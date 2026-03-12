from kafka import KafkaProducer
import json
import os

# Kafka configuration
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_ORDER_TOPIC", "order-topic")

# Initialize the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    linger_ms=5
)

def send_order_to_kafka(order_data: dict):
    """
    Send order data to Kafka topic (order-topic).
    """
    producer.send(KAFKA_TOPIC, value=order_data)
    producer.flush()
    print(f"✅ Sent to Kafka: {order_data}")
