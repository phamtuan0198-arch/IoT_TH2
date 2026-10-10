import pika
import time

# Kết nối tới RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Khai báo queue (đảm bảo queue tồn tại)
channel.queue_declare(queue='iot_lab_queue',durable=True)

def callback(ch, method, properties, body):
    current_time = time.strftime("%H:%M:%S")
    print(f"Da nhan message: {body.decode()}")
    print(f"Thoi gian nhan: {current_time}")

# Lắng nghe queue
channel.basic_consume(queue='iot_lab_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Consumer dang cho message. Nhan CTRL+C de thoat.')
channel.start_consuming()