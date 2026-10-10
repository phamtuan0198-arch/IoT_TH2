import pika
import json
import time
import random

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sensor_data_queue',durable=True)

try:
    while True:
        data = {
            "device_id": "sensor01",
            "temperature": round(random.uniform(25.0, 40.0), 1),
            "humidity": round(random.uniform(30.0, 70.0), 1)
        }
        
        channel.basic_publish(
            exchange='', 
            routing_key='sensor_data_queue', 
            body=json.dumps(data)
        )
        print(f" [x] Sent data: {data}")
        time.sleep(3) # Gửi mỗi 3 giây
except KeyboardInterrupt:
    connection.close()