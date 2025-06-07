import os
import time
import json
import requests
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

API_KEY = os.getenv("API_KEY")
CITIES = os.getenv("CITIES").split(',')
URL = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"

def create_producer():
    for i in range(10):
        try:
            print("Trying to connect to Kafka Producer...")
            producer = KafkaProducer(
                bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("Kafka Producer connected!")
            return producer
        except NoBrokersAvailable:
            print(f"No Kafka broker yet... retrying in 5 sec (attempt {i+1}/10)")
            time.sleep(5)
    raise Exception("Could not connect to Kafka after 10 tries.")
producer = create_producer()

def fetch_and_send():
    while True:
        for city in CITIES:
            try:
                print(f"Fetching weather for {city.strip()}...")
                response = requests.get(URL.format(city=city.strip(), key=API_KEY))
                data = response.json()
                if response.status_code == 200:
                    weather = {
                        'city': city.strip(),
                        'temp': data['main']['temp'],
                        'humidity': data['main']['humidity'],
                        'wind': data['wind']['speed'],
                        'pressure': data['main']['pressure'],
                        'timestamp': data['dt']
                    }
                    producer.send('weather', weather)
                    print(f"Sent weather data for {city.strip()} ✔")
                else:
                    print(f"Failed to fetch {city.strip()}: {data.get('message')}")
            except Exception as e:
                print(f"Error for {city.strip()}: {e}")
        time.sleep(60)

if __name__ == '__main__':
    fetch_and_send()
