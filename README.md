# 🚗 Real-time Traffic Data Producer (Kafka Setup)

## 📄 Description
This project simulates **real-time traffic data** (vehicle speed, location, time, etc.)  
and sends it continuously to a **Kafka topic** using a Python producer.  
The system runs a full local **Kafka cluster** using Docker.

---

## 📁 Files
| File | Description |
|------|--------------|
| `docker-compose.yml` | Starts Zookeeper, Kafka brokers, and Kafka UI. |
| `realtime_traffic_producer.py` | Python script generating and sending real-time traffic events. |
| `requirements.txt` | Contains Python dependencies (e.g., `kafka-python`, `faker`). |

---

## ⚙️ How to Run

1. Make sure **Docker Desktop** is running.  
2. Open a terminal or CMD in the project folder.  
3. Start Kafka containers:
   ```bash
   docker compose up -d