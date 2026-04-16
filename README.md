# HackBLR - Community Information Program (CIP) Assistant

## Project Overview
HackBLR is a voice-activated enterprise RAG (Retrieval-Augmented Generation) assistant designed to help process and retrieve information from the Community Information Program (CIP) dataset. This project includes a robust data preparation pipeline and a vector-based search system using Qdrant and Google Vertex AI.

---

## 🛠️ Components

### 1. HackBLR Voice App
A modern React-based voice assistant interface located in the `HackBLR/` directory.

### 2. Data Preparation & Versioning
Located in the root directory, these scripts ensure the CIP dataset is clean and versioned correctly.
*   **Data Cleaning:** Handles BOM removal, whitespace trimming, and missing value imputation.
*   **Versioning:** Automatically generates `Raw_Data_vYYYYMMDD_N.csv` to track data iterations.

### 3. Data Ingestion (`Data_Injector.py`)
This script processes the cleaned CSV data and uploads it to Qdrant Cloud or a local Qdrant instance.
*   **Embeddings:** Uses Google Vertex AI (`text-embedding-004`).
*   **Logic:** Converts structured patient data into readable "stories" for better semantic retrieval.
*   **Usage:** `python Data_Injector.py`

---

## 🚀 Setup & Verification

### 1. Configuration
Update your `.env` file with the following variables:
```env
GOOGLE_CLOUD_PROJECT=hackblr-493411
QDRANT_URL=https://f49166a3-8b8a-43af-b86a-b153f7884bd5.us-east4-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=enterprise_kb
```

### 2. Verify Qdrant Connection
Run the following script to ensure your Qdrant instance is reachable:
```bash
python check_qdrant.py
```

### 3. Inject Data
Once connected, upload your latest data:
```bash
python Data_Injector.py
```

---

## 📊 Data Preparation Details (April 15, 2026)
This project maintains a strict cleaning and normalization process for the `CIP_LATEST.csv` file:
*   **Normalized Structure:** Strict 85-column format.
*   **Latest Data File:** `Raw_Data_v20260415_2.csv` (201 Rows).
*   **Integrity:** Verified consistent column counts and header normalization.

---

## Usage Example (Python)
To load the latest data version in your own scripts:
```python
import os
from datetime import datetime

today = datetime.now().strftime("%Y%m%d")
pattern = f"Raw_Data_v{today}"
files = [f for f in os.listdir('.') if f.startswith(pattern)]
latest = sorted(files)[-1]
```
