# HackBLR - Tribal Mental Health AI & Community Assistant

## 🌟 Overview
 The deployment to Google Cloud Run was successful, and the live application is now updated!                                                                         
                                                                                                                                                                      
  Live Links                                                                                                                                                          
   - Main App: https://hackblr-app-rpfcyhqwsa-uc.a.run.app (https://hackblr-app-rpfcyhqwsa-uc.a.run.app)                                                              
   - Python API: https://hackblr-python-api-rpfcyhqwsa-uc.a.run.app (https://hackblr-python-api-rpfcyhqwsa-uc.a.run.app) 

---

## 🏗️ System Architecture

### 1. Frontend: Voice-Activated Assistant (`HackBLR/`)
A modern **React + Vite** application providing a seamless voice interface.
- **Vapi Integration:** Uses the Vapi SDK for real-time, low-latency voice interaction.
- **Live Transcript:** Displays real-time conversation between the user and the AI.
- **Deployment:** Hosted on **Google Cloud Run**, served via the Node.js API.

### 2. Node.js Search API (`HackBLR/api/`)
An **Express.js** backend that serves as a high-speed search layer for local community resources.
- **Local Database:** Connects to `data/mental_health_db.json` for FAQ and resource lookup.
- **Vapi Tool Endpoint:** Configured to handle direct tool calls from the Vapi voice assistant.
- **Deployment:** Hosted on **Google Cloud Run**.

### 3. Python Semantic Search API (`app/`)
A **FastAPI** service focused on deep semantic retrieval using Vector RAG.
- **Qdrant Backend:** Performs semantic search across the `enterprise_kb` collection.
- **Embedding Integration:** Leverages Google Vertex AI (`text-embedding-004`) for high-accuracy patient data retrieval.
- **Deployment:** Hosted on **Google Cloud Run**.

### 4. Database: Qdrant Vector DB
- **Deployment:** Hosted on a **Google Compute Engine (GCE)** VM (`e2-small`) with persistent storage.
- **Access:** Accessible via `http://34.31.164.38:6333`.

### 5. Security: Workload Identity & IAM
- **GCP IAM:** Uses Service Accounts with fine-grained permissions for Vertex AI and Artifact Registry.
- **SPIFFE/SPIRE (Optional):** Zero-trust workload identity configuration available in `spire/`.

---

## 🚀 Deployment (Google Cloud Platform)

The project is containerized using Docker and deployed to **Google Cloud Run**.

### **Infrastructure Components**
| Component | Service | URL |
| :--- | :--- | :--- |
| **Main App (UI + Node)** | Cloud Run | [https://hackblr-app-rpfcyhqwsa-uc.a.run.app](https://hackblr-app-rpfcyhqwsa-uc.a.run.app) |
| **Semantic API (Python)** | Cloud Run | [https://hackblr-python-api-rpfcyhqwsa-uc.a.run.app](https://hackblr-python-api-rpfcyhqwsa-uc.a.run.app) |
| **Vector DB (Qdrant)** | Compute Engine | [http://34.31.164.38:6333](http://34.31.164.38:6333) |

### **Deployment Scripts**
- `gcloud-setup-db.sh`: Automates GCE VM creation, firewall rules, and Qdrant container startup.
- `gcloud-deploy.sh`: Builds Docker images and deploys services to Cloud Run.

#### **Required Environment Variables**
- **Python API:** `QDRANT_URL`, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`.
- **Node API:** `PYTHON_API_URL`, `VITE_VAPI_PUBLIC_KEY`, `VITE_VAPI_ASSISTANT_ID`.

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
