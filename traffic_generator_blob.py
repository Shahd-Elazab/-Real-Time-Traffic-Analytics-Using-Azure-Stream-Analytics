# traffic_generator_blob.py
import os, time, json, random, datetime
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# load .env
load_dotenv()

# config
CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not CONN_STR:
    raise SystemExit("Missing AZURE_STORAGE_CONNECTION_STRING in .env")

CONTAINER = "raw-data"
PREFIX = "traffic/raw"   # files will land under this path in the container
SLEEP_SECONDS = 1        # send 1 event per second (change if you want faster)

# init client
blob_service = BlobServiceClient.from_connection_string(CONN_STR)
container_client = blob_service.get_container_client(CONTAINER)
if not container_client.exists():
    container_client.create_container()

print(f"Uploading events to container '{CONTAINER}' path '{PREFIX}/' every {SLEEP_SECONDS}s...")

try:
    while True:
        record = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "location": random.choice(["Cairo", "Alexandria", "Giza", "Mansoura", "Tanta"]),
            "vehicle_count": random.randint(10, 100),
            "avg_speed": round(random.uniform(20, 120), 2),
        }
        filename = f"{PREFIX}/traffic_{int(time.time())}.json"
        blob_client = container_client.get_blob_client(filename)
        blob_client.upload_blob(json.dumps(record), overwrite=True)
        print("✅ Uploaded:", filename, record)
        time.sleep(SLEEP_SECONDS)

except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")
