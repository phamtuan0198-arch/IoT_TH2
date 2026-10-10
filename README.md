# Bai tap RabbitMQ va IoT

## Gioi thieu

Repository gom 7 chuong trinh Python minh hoa giao tiep producer/consumer voi RabbitMQ:

- Bai 1: gui va nhan chuoi van ban qua queue `iot_lab_queue`.
- Bai 2: producer gui nhiet do va do am dang JSON; monitor doc va canh bao theo nguong.
- Bai 3: producer phat canh bao qua direct exchange; hai consumer nhan rieng muc `warning` va `critical`.

## Broker su dung

Cac chuong trinh su dung **RabbitMQ**, mot message broker noi bo giao tiep bang giao thuc AMQP. Thu vien Python `pika` mo ket noi toi `localhost` voi cau hinh mac dinh cua RabbitMQ (port AMQP `5672`, tai khoan mac dinh `guest`/`guest`). Cac script khong truyen username/password rieng, nen RabbitMQ can cho phep ket noi mac dinh tren may dang chay chuong trinh.

Can cai va khoi dong RabbitMQ truoc khi chay cac script. Neu dung Docker tren may local, chay lenh sau de mo port AMQP va cho phep tai khoan `guest` ket noi tu host:

```powershell
docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 -e RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS="-rabbit loopback_users []" rabbitmq:management
```

Neu container da duoc tao tu truoc, khoi dong lai bang `docker start rabbitmq`. Giao dien quan tri nam tai http://localhost:15672. Cau hinh tren chi phu hop cho bai tap local; khong mo cac port nay ra mang cong cong.

## Chuan bi Python

Mo PowerShell tai thu muc repository va cai thu vien:

```powershell
py -m pip install pika
```

Moi terminal can chay script phai dung cung moi truong Python da cai `pika`. Neu may khong co lenh `py`, thay bang `python`.

## Cach chay

Consumer thuong chay lien tuc, vi vay mo cac terminal rieng. Hay khoi dong consumer truoc producer de nhin thay message ngay khi gui. Dung consumer bang `Ctrl+C`.

### Bai 1: Queue co ban

Terminal 1:

```powershell
py consumer_bai1.py
```

Terminal 2:

```powershell
py producer_bai1.py
```

Producer gui mot message den queue `iot_lab_queue`, sau do ket thuc. Consumer in noi dung va thoi diem nhan, vi du:

```text
[x] Da gui: 'Xin chao tu ung dung Python AMQP - B23DCCN891 - Phạm Anh Tuấn'
Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN891 - Phạm Anh Tuấn
Thoi gian nhan: 14:25:03
```

Thoi gian hien thi phu thuoc luc chay. Chuoi co dau trong terminal co the hien thi khac tuy encoding.

### Bai 2: Du lieu sensor JSON

Terminal 1:

```powershell
py monitor_consumer_bai2.py
```

Terminal 2:

```powershell
py sensor_producer_bai2.py
```

Producer gui du lieu `sensor01` moi 3 giay va chay cho den khi nhan `Ctrl+C`. Monitor in nhiet do, do am; nhiet do tren `35` thi in canh bao nhiet do cao, do am duoi `40` thi in canh bao do am thap. Gia tri thay doi ngau nhien trong moi lan gui, vi du:

```text
[x] Sent data: {'device_id': 'sensor01', 'temperature': 37.2, 'humidity': 35.4}
Device: sensor01
Temperature: 37.2
Humidity: 35.4
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
```

### Bai 3: Canh bao qua direct exchange

Mo ba terminal. Chay hai consumer truoc:

```powershell
py warning_consumer_bai3.py
```

```powershell
py critical_consumer_bai3.py
```

Sau do chay producer trong terminal thu ba:

```powershell
py alert_producer_bai3.py
```

Producer khai bao exchange `iot_alert_exchange` loai `direct`, roi gui ba message voi routing key `info`, `warning`, `critical`. Queue `warning_queue` chi bind key `warning`, con `critical_queue` chi bind key `critical`. Ket qua:

```text
Producer:
[x] Da gui muc 'info': He thong hoat dong binh thuong
[x] Da gui muc 'warning': Nhiet do phong may vuot nguong warning
[x] Da gui muc 'critical': Cam bien kho lanh mat ket noi critical

warning consumer:
[warning_queue] Da nhan: Nhiet do phong may vuot nguong warning

critical consumer:
[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
```

Khong co queue nao bind routing key `info`, nen message `info` khong duoc dua vao queue va se bi bo qua. Thu tu output tren cac terminal consumer co the khac nhau.

## Danh sach chuong trinh

- `producer_bai1.py` va `consumer_bai1.py`: producer va consumer cho Bai 1.
- `sensor_producer_bai2.py` va `monitor_consumer_bai2.py`: producer va monitor cho Bai 2.
- `alert_producer_bai3.py`, `warning_consumer_bai3.py`, `critical_consumer_bai3.py`: producer va hai consumer cho Bai 3.

## Luu y

Cac queue trong cac script duoc khai bao `durable=True`, nhung cac message hien tai khong duoc publish voi che do persistent. Exchange cua Bai 3 cung khong khai bao durable. Vi vay, khong nen xem cac message nay la duoc dam bao ton tai qua lan khoi dong lai broker.