import os
import pandas as pd
from typing import List
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_google_vertexai import VertexAIEmbeddings

# 1. Load environment variables
load_dotenv()

# 2. Configuration
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1").strip()
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333").strip()
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "enterprise_kb").strip()

# 3. Initialize Clients
print(f"Connecting to Qdrant at {QDRANT_URL}...")
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

print("Initializing Vertex AI Embeddings...")
embeddings = VertexAIEmbeddings(
    model_name="text-embedding-004",
    project=GOOGLE_CLOUD_PROJECT,
    location=GOOGLE_CLOUD_LOCATION,
)

# 4. Ensure Qdrant collection exists
# Note: text-embedding-004 output dimension is 768
vector_size = 768 

if not client.collection_exists(QDRANT_COLLECTION):
    client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )
    print(f"Collection '{QDRANT_COLLECTION}' created!")

# 5. Load Source Data
csv_file_path = "Raw_Data_v20260415_2.csv"
print(f"Loading data from {csv_file_path}...")
df = pd.read_csv(csv_file_path)

# 6. Transformation Logic: Convert Row to Natural Language Summary
def create_patient_summary(row):
    """
    Transforms structured CSV row data into a natural language summary for semantic search.
    """
    summary = (
        f"Patient {row['Name']} (UHID: {row['UHID']}) is {row['Age_yrs']} years old and belongs to the {row['SUBTRIBE']} subtribe. "
        f"They reside {row['Dis_from_CIP_km']} km from CIP. "
        f"Their initial clinical contact for treatment was {row['First_Contact']}. "
        f"Prior to visiting CIP, they spent Rs {row['NonMed_Expense']} on non-medical treatments. "
        f"Regarding the cause of illness, their belief in witchcraft is recorded as: {row['SAQ_Witchcraft']}. "
        f"Substance use history: {row['Substance_Used']}."
    )
    return summary

# 7. Data Injection Process
points = []
print("Generating summaries and embeddings...")

# Utilize batching for efficient API interactions
summaries = []
payloads = []

for index, row in df.iterrows():
    row = row.fillna("Not specified")
    patient_text = create_patient_summary(row)
    summaries.append(patient_text)
    payloads.append({
        "uhid": row['UHID'],
        "name": row['Name'],
        "text": patient_text # 'text' key ensures compatibility with the search endpoint
    })

# Batch generation of embeddings
try:
    vectors = embeddings.embed_documents(summaries)
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
