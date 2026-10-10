import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='iot_alert_exchange', exchange_type='direct')

alerts = [
    ("info", "He thong hoat dong binh thuong"),
    ("warning", "Nhiet do phong may vuot nguong warning"),
    ("critical", "Cam bien kho lanh mat ket noi critical")
]

for routing_key, msg in alerts:
    channel.basic_publish(
        exchange='iot_alert_exchange',
        routing_key=routing_key,
        body=msg
    )
    print(f" [x] Da gui muc '{routing_key}': {msg}")

connection.close()