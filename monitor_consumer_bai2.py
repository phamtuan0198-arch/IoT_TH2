import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sensor_data_queue', durable=True)

def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    print(f"\nDevice: {data['device_id']}")
    print(f"Temperature: {data['temperature']}")
    print(f"Humidity: {data['humidity']}")
    
    if data['temperature'] > 35:
        print("CANH BAO: Nhiet do cao")
    if data['humidity'] < 40:
        print("CANH BAO: Do am thap")

channel.basic_consume(queue='sensor_data_queue', on_message_callback=callback, auto_ack=True)
print(' [*] Monitor dang cho du lieu sensor...')
channel.start_consuming()