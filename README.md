# 🎙️ HackBLR - Tribal Mental Health AI & Community Assistant

HackBLR is a high-performance AI ecosystem designed to bridge the digital divide for tribal populations. It combines **Real-time Voice AI**, **Semantic Vector Search**, and **Secure Workload Identity** to provide cultural-sensitive mental health support and local resource discovery.

**🔗 Live Web App:** [https://hackblr-app-rpfcyhqwsa-uc.a.run.app](https://hackblr-app-rpfcyhqwsa-uc.a.run.app)
**🔗 Semantic Search API:** [https://hackblr-python-api-rpfcyhqwsa-uc.a.run.app](https://hackblr-python-api-rpfcyhqwsa-uc.a.run.app)

---

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

## 🚀 Deployment

The project is fully automated for Google Cloud Platform.

```bash
# Set your project ID
gcloud config set project hackblr-493411

# Run the deployment script
bash gcloud-deploy.sh
```

---

## 🏆 HackBLR Bootcamp MVP
- **Mandatory Tech:** Strictly uses **Qdrant** and **Vapi**.
- **Security:** No API keys are committed; all configuration uses environment variables.
- **Branch:** `main`

---
*Built with ❤️ for the HackBLR Bootcamp.*
