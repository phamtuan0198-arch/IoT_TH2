import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Khai báo exchange loại direct
channel.exchange_declare(exchange='iot_alert_exchange', exchange_type='direct')
channel.queue_declare(queue='warning_queue',durable=True)

# Bind queue với exchange bằng routing key 'warning'
channel.queue_bind(exchange='iot_alert_exchange', queue='warning_queue', routing_key='warning')

def callback(ch, method, properties, body):
    print(f"[warning_queue] Da nhan: {body.decode()}")

channel.basic_consume(queue='warning_queue', on_message_callback=callback, auto_ack=True)
print(' [*] Cho canh bao muc WARNING...')
channel.start_consuming()