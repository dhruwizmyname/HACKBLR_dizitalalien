import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from langchain_google_vertexai import ChatVertexAI, VertexAIEmbeddings
from qdrant_client import QdrantClient

# Load env early
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

# SPIFFE Trust Domain Configuration
SPIFFE_TRUST_DOMAIN = os.getenv("SPIFFE_TRUST_DOMAIN", "example.org")

# Clients
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=30)

def get_embeddings_client() -> VertexAIEmbeddings:
    if not GOOGLE_CLOUD_PROJECT:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is missing. Update .env.")
    return VertexAIEmbeddings(
        model_name="text-embedding-004",
        project=GOOGLE_CLOUD_PROJECT,
        location=GOOGLE_CLOUD_LOCATION,
    )

def get_llm_client() -> ChatVertexAI:
    if not GOOGLE_CLOUD_PROJECT:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is missing. Update .env.")
    return ChatVertexAI(
        model_name="gemini-1.5-flash",
        project=GOOGLE_CLOUD_PROJECT,
        location=GOOGLE_CLOUD_LOCATION,
        temperature=0.2,
        max_output_tokens=500,
    )

def extract_text_from_payload(obj: Any) -> Optional[str]:
    priority_keys = ("message", "input", "transcript", "text", "query", "prompt", "utterance")
    if isinstance(obj, dict):
        for key in priority_keys:
            value = obj.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        for value in obj.values():
            found = extract_text_from_payload(value)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = extract_text_from_payload(item)
            if found:
                return found
    elif isinstance(obj, str) and obj.strip():
        return obj.strip()
    return None

def retrieve_context(user_text: str) -> List[str]:
    try:
        embeddings = get_embeddings_client()
        query_vec = embeddings.embed_query(user_text)
        hits = qdrant.search(
            collection_name=QDRANT_COLLECTION,
            query_vector=query_vec,
            limit=QDRANT_TOP_K,
            with_payload=True,
        )
        context = []
        for hit in hits:
            payload: Dict[str, Any] = hit.payload or {}
            txt = payload.get("text")
            if isinstance(txt, str) and txt.strip():
                context.append(txt.strip())
        return context
    except Exception as exc:
        logger.exception("Vector search failed: %s", exc)
        return []

def generate_answer(user_text: str, context_chunks: List[str]) -> str:
    llm = get_llm_client()
    context_block = (
        "\n\n".join(f"[Context {i + 1}] {chunk}" for i, chunk in enumerate(context_chunks))
        or "No matching context found."
    )
    prompt = f"""
You are an enterprise voice assistant. Answer concisely and conversationally for spoken output.
If context is insufficient, say so briefly and provide the best possible helpful response.

User question:
{user_text}

Retrieved context:
{context_block}
""".strip()

    try:
        result = llm.invoke(prompt)
        content = getattr(result, "content", "")
        return str(content).strip() if content else "I'm sorry, I couldn't generate a response."
    except Exception as exc:
        logger.exception("LLM generation failed: %s", exc)
        return "I'm having trouble connecting to my brain right now. Please try again later."

@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}

@app.post("/vapi-webhook")
async def vapi_webhook(request: Request) -> JSONResponse:
    try:
        payload = await request.json()
        user_text = extract_text_from_payload(payload) or payload.get("query")
        
        if not user_text:
            return JSONResponse({"error": "No query found."}, status_code=400)

        context = retrieve_context(user_text)
        answer = generate_answer(user_text, context)
        return JSONResponse({"response": answer})
    except Exception as e:
        logger.error(f"Webhook Error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)
