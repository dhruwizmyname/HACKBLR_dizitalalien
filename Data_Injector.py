import os
import pandas as pd
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# 1. Environment variables load karo
load_dotenv()

# 2. Qdrant Cloud & Embedding Model setup
print("Connecting to Qdrant Cloud...")
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)
model = SentenceTransformer('all-MiniLM-L6-v2')

collection_name = "garima_patients"

# 3. Collection create karo (agar nahi hai toh)
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    print(f"Collection '{collection_name}' created!")

# 4. Data Load karo
csv_file_path = "Garima_Project.xlsx - Garima_Project.csv" # Yahan apna sahi CSV path daalna
print(f"Loading data from {csv_file_path}...")
df = pd.read_csv(csv_file_path)

# 5. The "Magic" Function: Row ko Story mein badalna
def create_patient_summary(row):
    """
    Yeh function PDF questionnaire ke context ko CSV variables ke saath jodata hai.
    Taaki LLM ko pura context samajh aaye.
    """
    summary = (
        f"Patient UHID {row['UHID']} is {row['Age']} years old and belongs to the {row['SUBTRIBE']} subtribe. "
        f"They live {row['Dis_from_CIP']} km away from CIP. "
        f"Their first contact for treatment was {row['First_Contact']}. "
        f"Before visiting CIP, they spent Rs {row['NonMed_Expense']} on non-medical treatments. "
        f"When asked about the cause of illness, their belief in witchcraft is recorded as: {row['SAQ_Witchcraft']}. "
        f"Substance used: {row['Substance_Used']}."
    )
    return summary

# 6. Data Inject Process
points = []
for index, row in df.iterrows():
    # NaN ya missing values ko blank string se replace karo taaki error na aaye
    row = row.fillna("Not specified")
    
    # Text summary banao
    patient_text = create_patient_summary(row)
    
    # Text ko Vector mein badlo
    vector = model.encode(patient_text).tolist()
    
    # Qdrant Point create karo (Payload mein original data bhi rakh rahe hain)
    point = PointStruct(
        id=index + 1,  # Qdrant ko unique ID chahiye
        vector=vector,
        payload={
            "uhid": row['UHID'],
            "age": row['Age'],
            "semantic_text": patient_text # Yeh Vapi Agent padhega
        }
    )
    points.append(point)

# 7. Upload to Qdrant
print(f"Uploading {len(points)} records to Qdrant...")
client.upsert(
    collection_name=collection_name,
    points=points
)
print("Data Injection Successful! 🎉")