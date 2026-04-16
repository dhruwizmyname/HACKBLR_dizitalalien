import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

print(f"Attempting to connect to Qdrant at: {qdrant_url}")

client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)

try:
    collections = client.get_collections()
    print("✅ Connected to Qdrant!")
    print(f"Collections: {[c.name for c in collections.collections]}")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
