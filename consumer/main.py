import json
from kafka import KafkaConsumer
import pandas as pd
import os
import time
from kafka.errors import NoBrokersAvailable

# Retry mechanism for connecting to Kafka
def create_consumer():
    for i in range(10):  # Retry up to 10 times
        try:
            print("Attempting to connect to Kafka...")
            consumer = KafkaConsumer(
                'weather',
                bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
                auto_offset_reset='earliest',
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            print("Connected to Kafka!")
            return consumer
        except NoBrokersAvailable:
            print(f"Kafka not available yet... retrying in 5 seconds (try {i+1}/10)")
            time.sleep(5)
    raise Exception("Could not connect to Kafka after 10 tries.")

data = []

def consume():
    os.makedirs('/data', exist_ok=True)
    consumer = create_consumer()
    print("Consumer waiting for messages on 'weather' topic...")

    for msg in consumer:
        record = msg.value
        print(f"Received message: {record}")
        data.append(record)
        pd.DataFrame(data).drop_duplicates().to_csv('/data/weather_data.csv', index=False)
        print(f"Saved data for {record['city']}")

if __name__ == '__main__':
    consume()
