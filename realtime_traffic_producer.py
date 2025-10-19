import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

# إعدادات Kafka
TOPIC = "traffic_data"
BOOTSTRAP_SERVERS = ["localhost:19092"]  # ✅ الاتصال من Windows بـ Kafka داخل Docker

# إنشاء منتج Kafka
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print(f"🚀 Starting real-time data generation to topic '{TOPIC}' (5 msg/s)")

try:
    while True:
        # توليد بيانات وهمية عن حركة المرور
        event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "timestamp": event_time,
            "location": random.choice(["Cairo", "Alexandria", "Giza", "Mansoura", "Tanta"]),
            "vehicle_count": random.randint(10, 100),
            "avg_speed": round(random.uniform(20, 120), 2),
        }

        # إرسال البيانات إلى Kafka
        producer.send(TOPIC, value=record)
        print(f"✅ Sent: {record}")

        # إرسال 5 رسائل في الثانية → يعني فاصل 0.2 ثانية بين كل رسالة
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")
finally:
    producer.close()
    print("✅ Producer closed safely.")

