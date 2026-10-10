import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='iot_alert_exchange', exchange_type='direct')
channel.queue_declare(queue='critical_queue',durable=True)

# Bind queue với routing key 'critical'
channel.queue_bind(exchange='iot_alert_exchange', queue='critical_queue', routing_key='critical')

def callback(ch, method, properties, body):
    print(f"[critical_queue] Da nhan: {body.decode()}")

channel.basic_consume(queue='critical_queue', on_message_callback=callback, auto_ack=True)
print(' [*] Cho canh bao muc CRITICAL...')
channel.start_consuming()