# 🎙️ HackBLR - Tribal Mental Health AI & Community Assistant

HackBLR is a high-performance AI ecosystem designed to bridge the digital divide for tribal populations. It combines **Real-time Voice AI**, **Semantic Vector Search**, and **Secure Workload Identity** to provide cultural-sensitive mental health support and local resource discovery.

> [!CAUTION]
> **Project Status: Archived / Offline** > The live cloud deployments (Cloud Run & Compute Engine) have been taken down to minimize infrastructure costs. As this project is a non-commercial MVP/Bootcamp prototype, the live URLs are no longer active.

## 🏗️ System Architecture

### 1. Frontend: Voice-Activated Assistant (`HackBLR/`)
A modern **React + Vite** application providing a seamless voice interface.
- **Vapi.ai Web SDK:** Real-time, low-latency conversational AI.
- **Live Transcript:** Displays conversational feed between user and AI.
- **Modern UI:** Glassmorphism UI with CSS voice visualizers.

### 2. Semantic Search Engine (`app/`)
A high-speed **FastAPI** service for clinical retrieval using Vector RAG.
- **Qdrant Vector Database:** Manages high-dimensional clinical data embeddings.
- **Vertex AI Embeddings:** Powered by Google's `text-embedding-004`.
- **RAG Implementation:** Maps clinical codes into semantic summaries for LLM processing.

### 3. Integrated Resource API (`HackBLR/api/`)
An **Express.js** backend serving community resources and local mental health data.

---

## 🛠️ Technology Stack

| Component | Technology | Use Case |
| :--- | :--- | :--- |
| **Voice AI** | [Vapi.ai](https://vapi.ai) | Conversational Agent & STT/TTS Pipeline |
| **Vector DB** | [Qdrant](https://qdrant.tech) | Storing and Querying Clinical Embeddings |
| **LLM/Embeddings** | [Google Vertex AI](https://cloud.google.com/vertex-ai) | Generating semantic vector representations |
| **Compute** | [Google Cloud Run](https://cloud.google.com/run) | Serverless Hosting for APIs and Frontend |
| **Cloud DB** | [Google Compute Engine](https://cloud.google.com/compute) | Hosting Persistent Qdrant Instance |
| **Backend (Python)** | FastAPI | Semantic Search & RAG Orchestration |
| **Backend (Node)** | Express.js | Static serving & Resource lookup |
| **Frontend** | React + Vite | User Interface & Vapi SDK Integration |
| **Security** | SPIFFE/SPIRE | Zero-trust workload identity (Optional) |
| **Infrastructure** | Docker | Containerization of all services |

---

## 🚀 Local Deployment & Setup

### 1. Prerequisites
- **Docker:** Required for running the Qdrant Vector Database.
- **Python 3.10+:** For the Semantic Search API.
- **Node.js 20+:** For the Frontend and Resource API.

### 2. Startup Procedure

#### Step A: Start Qdrant (Vector Database)
```bash
docker run -d -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

#### Step B: Inject Clinical Data
Ensure your `.env` has the correct `GOOGLE_API_KEY` (from Google AI Studio) and run:
```bash
python local_data_injector.py
```
*Note: This uses local embeddings (384-dim) for cost-efficiency and speed.*

#### Step C: Start Semantic Search API (Python)
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Step D: Start Frontend & Resource API (Node.js)
```bash
cd HackBLR
npm install
npm run backend  # Starts Express server on port 3001
npm run dev      # Starts Vite Frontend on port 5173
```

---

## 🛠️ Asset Management (React)
To prevent **404 Not Found** errors, always import assets directly in your components:
```javascript
import heroImage from './assets/hero.png';
// Use as: <img src={heroImage} />
```

---

## 🏆 Current Status
- ✅ **Local RAG:** Fully functional using Qdrant + SentenceTransformers.
- ✅ **Frontend:** Modernized React + Vite UI with proper asset bundling.
- ⚠️ **LLM:** Currently using Gemini 1.5 via Google AI Studio (requires valid `GOOGLE_API_KEY`).

---
*Built for -Love by @dizitalalien
