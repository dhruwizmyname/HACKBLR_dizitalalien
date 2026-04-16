from fastapi import FastAPI, Request
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

@app.post("/search_patient")
async def search_patient(request: Request):
    data = await request.json()
    query_text = data.get("query") # Vapi will send the user's voice query here
    
    # Execute semantic search via Qdrant
    search_result = client.search(
        collection_name="enterprise_kb",
        query_text=query_text,
        limit=1
    )
    
    if search_result:
        return {"results": search_result[0].payload['text']}
    return {"results": "No patient data found for this query."}