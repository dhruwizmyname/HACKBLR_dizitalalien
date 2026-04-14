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

# Placeholder: set these in .env with your actual values.
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()  # <- your GCP project ID
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1").strip()
VAPI_WEBHOOK_SECRET = os.getenv("VAPI_WEBHOOK_SECRET", "").strip()  # <- your VAPI shared secret

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333").strip()
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "enterprise_kb").strip()
QDRANT_TOP_K = int(os.getenv("QDRANT_TOP_K", "5"))

qdrant = QdrantClient(url=QDRANT_URL, timeout=30)


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


def validate_vapi_secret(x_vapi_secret: Optional[str], authorization: Optional[str]) -> None:
    if not VAPI_WEBHOOK_SECRET:
        return

    incoming = (x_vapi_secret or "").strip()
    if not incoming and authorization and authorization.lower().startswith("bearer "):
        incoming = authorization[7:].strip()

    if incoming != VAPI_WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized webhook request.")


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
    except Exception as exc:
        logger.exception("Vector search failed: %s", exc)
        raise HTTPException(status_code=502, detail="Failed to query enterprise knowledge base.")

    context = []
    for hit in hits:
        payload: Dict[str, Any] = hit.payload or {}
        txt = payload.get("text")
        if isinstance(txt, str) and txt.strip():
            context.append(txt.strip())
    return context


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
    except Exception as exc:
        logger.exception("LLM generation failed: %s", exc)
        raise HTTPException(status_code=502, detail="Failed to generate response from LLM.")

    content = getattr(result, "content", "")
    if isinstance(content, str):
        answer = content.strip()
    elif isinstance(content, list):
        answer = " ".join(str(x) for x in content).strip()
    else:
        answer = str(content).strip()

    if not answer:
        raise HTTPException(status_code=502, detail="LLM returned an empty response.")
    return answer


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/vapi-webhook")
async def vapi_webhook(
    request: Request,
    x_vapi_secret: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
) -> JSONResponse:
    validate_vapi_secret(x_vapi_secret, authorization)

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload.")

    user_text = extract_text_from_payload(payload)
    if not user_text:
        raise HTTPException(status_code=400, detail="No user text found in VAPI payload.")

    context = retrieve_context(user_text)
    answer = generate_answer(user_text, context)

    # VAPI spoken reply payload: plain text in a JSON field.
    return JSONResponse({"response": answer})
