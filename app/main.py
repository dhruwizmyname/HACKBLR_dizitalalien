import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI # Swapped from VertexAI

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-rag")

app = FastAPI(title="Voice-Activated Enterprise RAG Assistant (Local Edition)", version="1.0.0")

# ---------------- CONFIGURATION ----------------
# Removed GCP Project dependencies to fix 403 errors
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip() # Use a free key from aistudio.google.com
VAPI_WEBHOOK_SECRET = os.getenv("VAPI_WEBHOOK_SECRET", "").strip()
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333").strip()
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "").strip()
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "enterprise_kb").strip() # Pointing to your CIP dataset
QDRANT_TOP_K = int(os.getenv("QDRANT_TOP_K", "5"))

# ---------------- INITIALIZATION ----------------
logger.info("Connecting to Qdrant...")
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=30)

logger.info("Loading FREE Local Embedding Model (all-MiniLM-L6-v2)...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
logger.info("Local embedding model loaded successfully!")

# ---------------- ROUTES & LOGIC ----------------
@app.get("/")
def read_root():
    return {"message": "HackBLR Python Semantic Search API is running locally!"}

@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}

def get_llm_client() -> ChatGoogleGenerativeAI:
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is missing. Please add it to your .env file.")
    # Using the standard free API tier, bypassing GCP enterprise permissions
    return ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY, temperature=0.2)

def extract_text_from_payload(obj: Any) -> Optional[str]:
    priority_keys = ("message", "input", "transcript", "text", "query", "prompt", "utterance")
    if isinstance(obj, dict):
        for key in priority_keys:
            value = obj.get(key)
            if isinstance(value, str) and value.strip(): return value.strip()
        for value in obj.values():
            found = extract_text_from_payload(value)
            if found: return found
    return None

def retrieve_context(user_text: str) -> List[str]:
    try:
        # Generate Embeddings LOCALLY (No Google Cloud API Call!)
        query_vec = embedding_model.encode(user_text).tolist()
        
        # Search Qdrant (Note: Ensure your collection is now 384 dimensions)
        hits = qdrant.search(
            collection_name=QDRANT_COLLECTION, 
            query_vector=query_vec, 
            limit=QDRANT_TOP_K
        )
        results = [hit.payload.get("text", "") for hit in hits if hit.payload]
        logger.info(f"Retrieved {len(results)} context chunks from Qdrant.")
        for i, res in enumerate(results):
            logger.info(f"Chunk {i+1}: {res[:100]}...")
        return results
    except Exception as e:
        logger.error(f"Error retrieving context from Qdrant: {e}")
        return []

def generate_answer(user_text: str, context_chunks: List[str]) -> str:
    llm = get_llm_client()
    context_block = "\n\n".join(context_chunks) or "No context found in local database."
    prompt = f"User: {user_text}\nContext: {context_block}\nAnswer concisely and supportively for a mental health query:"
    
    try:
        result = llm.invoke(prompt)
        return str(result.content).strip()
    except Exception as e:
        logger.error(f"LLM Generation Error: {e}")
        return "Service temporarily unavailable."

@app.post("/vapi-webhook")
async def vapi_webhook(request: Request) -> JSONResponse:
    try:
        payload = await request.json()
        
        # Extract speech text coming from the Vapi Assistant
        user_text = extract_text_from_payload(payload) or payload.get("query")
        if not user_text: 
            return JSONResponse({"error": "No query found."}, status_code=400)
            
        # Run RAG Pipeline
        context = retrieve_context(user_text)
        answer = generate_answer(user_text, context)
        
        # Return to Vapi
        return JSONResponse({"response": answer})
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)