# 🚦 Real-time Traffic Data Streaming & Analytics

## 📄 Description
This project simulates **real-time traffic data** (speed, vehicle count, location, timestamp)  
and streams it through **Apache Kafka**.  
Then, **Apache Spark Structured Streaming** reads and analyzes the data in real time —  
aggregating the **average speed** and **total vehicles per location** every minute  
and saving the results into CSV files.

---

## 📁 Files
| File | Description |
|------|--------------|
| `docker-compose.yml` | Starts Kafka, Zookeeper, and Jupyter Spark containers using Docker. |
| `work/realtime_traffic_producer.py` | Python script generating and sending live traffic data to Kafka (located inside the `work/` folder). |
| `traffic_stream_analytics.py` | Spark Structured Streaming job reading from Kafka and performing analytics. |
| `traffic_analytics/` | Folder where Spark stores real-time CSV analytics output. |
| `analytics_checkpoints/` | Folder for Spark streaming checkpoints (state tracking). |

---

## ⚙️ How to Run

1. Make sure **Docker Desktop** is running.  
2. Open a terminal inside your project folder.  
3. Start all containers:
   ```bash
   docker compose up -d
