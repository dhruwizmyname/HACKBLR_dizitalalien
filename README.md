# HackBLR - Tribal Mental Health AI & Community Assistant

## 🌟 Overview
HackBLR is a comprehensive AI-driven ecosystem designed for the **Tribal Mental Health Database** and the **Community Information Program (CIP)**. It combines voice-activated AI, semantic search, and secure workload identity to provide a robust platform for information retrieval and mental health support.

**🔗 Live Web App:** [https://cautious-space-enigma-7r4vg5wvrrgfx4jr-5173.app.github.dev/](https://cautious-space-enigma-7r4vg5wvrrgfx4jr-5173.app.github.dev/)

---

## 🏗️ System Architecture

### 1. Frontend: Voice-Activated Assistant (`HackBLR/`)
A modern **React + Vite** application providing a seamless voice interface.
- **Vapi Integration:** Uses the Vapi SDK for real-time, low-latency voice interaction.
- **Live Transcript:** Displays real-time conversation between the user and the AI.

### 2. Node.js Search API (`HackBLR/api/`)
An **Express.js** backend that serves as a high-speed search layer for local community resources.
- **Local Database:** Connects to `data/mental_health_db.json` for FAQ and resource lookup.
- **Vapi Tool Endpoint:** Configured to handle direct tool calls from the Vapi voice assistant.

### 3. Python Semantic Search API (`app/`)
A **FastAPI** service focused on deep semantic retrieval using Vector RAG.
- **Qdrant Backend:** Performs semantic search across the `enterprise_kb` collection.
- **Embedding Integration:** Leverages Google Vertex AI (`text-embedding-004`) for high-accuracy patient data retrieval.

### 4. Security: SPIFFE/SPIRE (`spire/`)
Zero-trust workload identity for secure service-to-service communication.
- **Trust Domain:** `example.org`
- **Identity Issuance:** Short-lived SVIDs for the Node.js and Python APIs to communicate without hardcoded secrets.

---

## 🚀 Deployment (Render)

### Live Hosting Configuration
The project is configured for automated deployment via **Render** from the `main` branch using `render.yaml`.

#### **Service Settings**
| Service | Build Command | Start Command |
| :--- | :--- | :--- |
| **Frontend** | `cd HackBLR && npm install && npm run build` | (Static Site) |
| **Node API** | `cd HackBLR && npm install` | `cd HackBLR && node api/server.js` |
| **Python API** | `pip install -r requirements.txt` | `uvicorn app.main:app --host 0.0.0.0 --port 10000` |

#### **Required Environment Variables**
- **Frontend:** `VITE_VAPI_PUBLIC_KEY`, `VITE_VAPI_ASSISTANT_ID`
- **Node API:** `PYTHON_API_URL` (URL of your live Python service + `/vapi-webhook`)
- **Python API:** `QDRANT_URL`, `QDRANT_API_KEY`, `GOOGLE_CLOUD_PROJECT`

---

## 🛠️ Development Setup

1. **Install Dependencies:**
   ```bash
   # Install Node.js dependencies
   cd HackBLR && npm install

   # Install Python dependencies (from root)
   pip install -r requirements.txt
   ```

2. **Start the Services Locally:**

   - **Option A: Run Frontend (Vite Dev Mode)**
     ```bash
     cd HackBLR
     npm run dev
     ```

   - **Option B: Run Node.js API (Backend)**
     ```bash
     cd HackBLR
     npm start
     ```

   - **Option C: Run Python Semantic API**
     ```bash
     uvicorn app.main:app --reload
     ```

3. **Verify Vector Search:**
   ```bash
   python check_qdrant.py
   ```

---

## 📊 Data Normalization (Latest: April 15, 2026)
We maintain a strict 85-column normalization process for all Community Information Program datasets to ensure consistency across AI models and retrieval systems.
