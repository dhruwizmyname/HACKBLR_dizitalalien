import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from langchain_google_vertexai import ChatVertexAI, VertexAIEmbeddings
from qdrant_client import QdrantClient

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-rag")

app = FastAPI(title="Voice-Activated Enterprise RAG Assistant", version="1.0.0")

# Configuration
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1").strip()
VAPI_WEBHOOK_SECRET = os.getenv("VAPI_WEBHOOK_SECRET", "").strip()
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333").strip()
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "").strip()
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "enterprise_kb").strip()
QDRANT_TOP_K = int(os.getenv("QDRANT_TOP_K", "5"))

qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=30)

@app.get("/")
def read_root():
    return {"message": "HackBLR Python Semantic Search API is running"}

@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}

def get_embeddings_client() -> VertexAIEmbeddings:
    if not GOOGLE_CLOUD_PROJECT:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is missing.")
    return VertexAIEmbeddings(model_name="text-embedding-004", project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)

def get_llm_client() -> ChatVertexAI:
    return ChatVertexAI(model_name="gemini-1.5-flash", project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION, temperature=0.2)

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
        embeddings = get_embeddings_client()
        query_vec = embeddings.embed_query(user_text)
        hits = qdrant.search(collection_name=QDRANT_COLLECTION, query_vector=query_vec, limit=QDRANT_TOP_K)
        return [hit.payload.get("text", "") for hit in hits if hit.payload]
    except Exception:
        return []

def generate_answer(user_text: str, context_chunks: List[str]) -> str:
    llm = get_llm_client()
    context_block = "\n\n".join(context_chunks) or "No context found."
    prompt = f"User: {user_text}\nContext: {context_block}\nAnswer concisely:"
    try:
        result = llm.invoke(prompt)
        return str(result.content).strip()
    except Exception:
        return "Service temporarily unavailable."

@app.post("/vapi-webhook")
async def vapi_webhook(request: Request) -> JSONResponse:
    try:
        payload = await request.json()
        user_text = extract_text_from_payload(payload) or payload.get("query")
        if not user_text: return JSONResponse({"error": "No query found."}, status_code=400)
        context = retrieve_context(user_text)
        answer = generate_answer(user_text, context)
        return JSONResponse({"response": answer})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
