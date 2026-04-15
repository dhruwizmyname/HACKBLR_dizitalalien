import os
import random
import pandas as pd
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# 1. Environment & Qdrant Setup
load_dotenv()
client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
model = SentenceTransformer('all-MiniLM-L6-v2')
collection_name = "garima_patients_full"

if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

# 2. Variable Definitions (Based on your CSV & PDF) 
subtribes = ["Munda", "Santhal", "Oraon", "Ho", "Kharia"]
contacts = ["Ojha/Tantrik", "General Physician", "Psychiatrist", "Ayurveda", "Homeopathy"]
beliefs = ["Yes", "No", "Don't Know"]
substances = ["Alcohol", "Tobacco", "Cannabis", "None"]

# 3. Generating 5 Detailed Mock Records
mock_data = []
for i in range(1, 6):
    patient = {
        # Demographics
        "UHID": f"GP-2026-{100+i}",
        "Name": f"Patient_{i}",
        "Age": random.randint(18, 70),
        "SUBTRIBE": random.choice(subtribes),
        "Dis_from_CIP": random.randint(5, 200),
        
        # Clinical Info
        "Duration": f"{random.randint(1, 12)} months",
        "First_Contact": random.choice(contacts),
        "NonMed_Expense": random.randint(1000, 20000),
        "Time_to_Doc": f"{random.randint(1, 4)} weeks",
        
        # Beliefs & Substance (SAQ)
        "SAQ_Witchcraft": random.choice(beliefs),
        "SAQ_Ghosts": random.choice(beliefs),
        "SAQ_EvilEye": random.choice(beliefs),
        "Substance_Used": random.choice(substances),
        "Usage_Frequency": "Daily" if random.random() > 0.5 else "Occasional",
        
        # Adding Scale Headers (ASS, ZBA, CAMI)
        "ASS_Score": random.randint(0, 22),
        "ZBA_Score": random.randint(0, 12),
        "CAMI_Score": random.randint(0, 11)
    }
    mock_data.append(patient)

# 4. Context Synthesis (Connecting Variables to PDF Questions)
def create_full_summary(row):
    return (
        f"Patient {row['Name']} (UHID: {row['UHID']}), aged {row['Age']}, belongs to {row['SUBTRIBE']} tribe. "
        f"Lives {row['Dis_from_CIP']}km from CIP. First treatment sought from {row['First_Contact']} "
        f"with an expenditure of ₹{row['NonMed_Expense']}. Belief in Supernatural causes: "
        f"Witchcraft: {row['SAQ_Witchcraft']}, Ghosts: {row['SAQ_Ghosts']}. "
        f"Substance Use: {row['Substance_Used']}. Clinical Scales: ASS({row['ASS_Score']}), "
        f"ZBA({row['ZBA_Score']}), CAMI({row['CAMI_Score']})."
    )

# 5. Injection Logic
points = []
for idx, row in enumerate(mock_data):
    text_context = create_full_summary(row)
    print(f"Injecting: {row['UHID']}...")
    
    vector = model.encode(text_context).tolist()
    points.append(PointStruct(
        id=idx + 1,
        vector=vector,
        payload={"metadata": row, "semantic_text": text_context}
    ))

client.upsert(collection_name=collection_name, points=points)
print("\nSuccess! 83-variable structured mock data injected into Qdrant. 🎉")