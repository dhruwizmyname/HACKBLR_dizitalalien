import os
import pandas as pd
from typing import List
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# 1. Load environment variables
load_dotenv()

# 2. Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333").strip()
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "").strip()
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "enterprise_kb").strip()

# 3. Initialize Clients
print(f"Connecting to Qdrant at {QDRANT_URL}...")
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

print("Loading local embedding model (all-MiniLM-L6-v2)...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
vector_size = 384 

# 4. Ensure Qdrant collection exists
if not client.collection_exists(QDRANT_COLLECTION):
    client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )
    print(f"Collection '{QDRANT_COLLECTION}' created!")
else:
    print(f"Collection '{QDRANT_COLLECTION}' already exists.")

# 5. Load Source Data
csv_file_path = "Final_Data.csv"
if not os.path.exists(csv_file_path):
    print(f"Error: {csv_file_path} not found.")
    exit(1)

print(f"Loading data from {csv_file_path}...")
df = pd.read_csv(csv_file_path)

# 6. Transformation Logic: Convert Row to Natural Language Summary
def create_patient_summary(row):
    """
    Transforms structured CSV row data into a natural language summary for semantic search.
    """
    summary = (
        f"Patient {row.get('Name', 'Unknown')} (UHID: {row.get('UHID', 'N/A')}) is {row.get('Age_yrs', 'N/A')} years old, gender {row.get('Gender', 'N/A')}, and belongs to the {row.get('SUBTRIBE', 'N/A')} subtribe. "
        f"They reside {row.get('Dis_from_CIP_km', 'N/A')} km from CIP. "
        f"Initial clinical contact: {row.get('First_Contact', 'N/A')}. Duration of illness: {row.get('Duration_days', 'N/A')} days. "
        f"Prior non-medical expense: Rs {row.get('NonMed_Expense', 'N/A')}. "
        f"Beliefs: Witchcraft ({row.get('SAQ_Witchcraft', 'N/A')}), Ghosts ({row.get('SAQ_Ghosts', 'N/A')}), Evil Eye ({row.get('SAQ_EvilEye', 'N/A')}). "
        f"Substance use: {row.get('Substance_Used', 'N/A')} (Frequency: {row.get('Usage_Frequency', 'N/A')}). "
        f"Other illnesses: {row.get('Other_illness', 'N/A')}."
    )
    return summary

# 7. Data Injection Process
points = []
print("Generating summaries and embeddings...")

summaries = []
payloads = []

for index, row in df.iterrows():
    row = row.fillna("Not specified")
    patient_text = create_patient_summary(row)
    summaries.append(patient_text)
    payloads.append({
        "uhid": row.get('UHID', 'N/A'),
        "name": row.get('Name', 'Unknown'),
        "text": patient_text 
    })

# Batch generation of embeddings
try:
    vectors = embedding_model.encode(summaries).tolist()
except Exception as e:
    print(f"Error generating embeddings: {e}")
    exit(1)

for i, (vector, payload) in enumerate(zip(vectors, payloads)):
    point = PointStruct(
        id=i + 1,
        vector=vector,
        payload=payload
    )
    points.append(point)

# 8. Upsert to Qdrant
print(f"Uploading {len(points)} records to Qdrant collection '{QDRANT_COLLECTION}'...")
client.upsert(
    collection_name=QDRANT_COLLECTION,
    points=points
)
print("Data Injection Successful! 🎉")
