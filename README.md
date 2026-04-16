# HackBLR - Tribal Mental Health AI & Community Assistant

## 🌟 Overview
HackBLR is a comprehensive AI-driven ecosystem designed for the **Tribal Mental Health Database** and the **Community Information Program (CIP)**. It combines voice-activated AI, semantic search, and secure workload identity to provide a robust platform for information retrieval and mental health support.

---

## 🏗️ System Architecture

### 1. Frontend: Voice-Activated Assistant (`HackBLR/`)
A modern **React + Vite** application providing a seamless voice interface.
- **Vapi Integration:** Uses the Vapi SDK for real-time, low-latency voice interaction.
- **Live Transcript:** Displays real-time conversation between the user and the AI.
- **Dynamic Styling:** Responsive UI designed for ease of use in community settings.

### 2. Node.js Search API (`HackBLR/api/`)
An **Express.js** backend that serves as a high-speed search layer for local community resources.
- **Local Database:** Connects to `data/mental_health_db.json` for FAQ and resource lookup.
- **Vapi Tool Endpoint:** Configured to handle direct tool calls from the Vapi voice assistant.

### 3. Python Semantic Search API (`app/`)
A **FastAPI** service focused on deep semantic retrieval using Vector RAG.
- **Qdrant Backend:** Performs semantic search across the `enterprise_kb` collection.
- **Embedding Integration:** Leverages Google Vertex AI (`text-embedding-004`) for high-accuracy patient data retrieval.

### 4. Data Pipeline (`root/`)
A robust workflow for cleaning and versioning sensitive community data.
- **`Data_Injector.py`:** Processes CSV data, converts records into semantic "stories," and injects them into the Qdrant Vector Cloud.
- **Data Versioning:** Automatically tracks data iterations (e.g., `Raw_Data_vYYYYMMDD_N.csv`) ensuring data integrity and rollback capability.

### 5. Security: SPIFFE/SPIRE (`spire/`)
Zero-trust workload identity for secure service-to-service communication.
- **Trust Domain:** `example.org`
- **Identity Issuance:** Short-lived SVIDs for the Node.js and Python APIs to communicate without hardcoded secrets.

---

## 🚀 Deployment

### Live Hosting
The project is configured for automated deployment via **Render** from the `main` branch.
- **`render.yaml`:** Orchestrates the deployment of the Frontend, Node API, and Python API as a unified blueprint.
- **Branch Strategy:** Development occurs on the `Dhruw-Shekhar` branch, while the `main` branch serves as the production host.

### Environment Configuration
Required `.env` variables for full system functionality:
```env
# Vapi
VITE_VAPI_PUBLIC_KEY=your-vapi-key
VITE_VAPI_ASSISTANT_ID=your-assistant-id

# Qdrant & Google Cloud
GOOGLE_CLOUD_PROJECT=hackblr-493411
QDRANT_URL=your-qdrant-url
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=enterprise_kb
```

---

## 🛠️ Development Setup

1. **Install Dependencies:**
   ```bash
   cd HackBLR && npm install
   pip install -r requirements.txt
   ```

2. **Run Frontend (Dev Mode):**
   ```bash
   npm run dev
   ```

3. **Verify Vector Search:**
   ```bash
   python check_qdrant.py
   ```

4. **Run Node Backend:**
   ```bash
   npm run backend
   ```

---

## 📊 Data Normalization (Latest: April 15, 2026)
We maintain a strict 85-column normalization process for all Community Information Program datasets to ensure consistency across AI models and retrieval systems.
