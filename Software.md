# HackBLR Software Documentation

This document provides a technical overview of the primary software components driving the HackBLR Tribal Mental Health AI ecosystem.

---

## 🎙️ Vapi AI: The Voice Orchestration Layer

Vapi acts as the interactive interface between the user and the mental health database. It manages the entire voice-to-data-to-voice lifecycle.

### Key Responsibilities:
1.  **Real-Time Speech-to-Text (STT):** Captures spoken input from the web interface, filters background noise, and performs high-accuracy transcription.
2.  **Autonomous Tool Calling:** Vapi is configured to interact with the project's **Node.js API (`HackBLR/api/server.js`)**. When a user asks a data-specific question, Vapi automatically triggers a tool call to the `/search_patient` endpoint.
3.  **Contextual Logic (LLM):** Once the database returns raw patient summaries, Vapi uses a Large Language Model (e.g., GPT-4) to synthesize that data into a natural, empathetic response.
4.  **Low-Latency Text-to-Speech (TTS):** Converts the synthesized response into human-like speech, ensuring the conversation feels fluid and responsive.

### Implementation Detail:
The frontend (`HackBLR/src/App.jsx`) utilizes the `@vapi-ai/web` SDK to manage the session, while the backend provides the necessary "Functions" for Vapi to execute search queries.

---

## 🔎 Qdrant: The Semantic Vector Database

Qdrant is the "brain" where the project's clinical data is stored. Unlike traditional SQL databases that search for exact keywords, Qdrant searches for **meaning and context**.

### Key Responsibilities:
1.  **Vector Similarity Search:** Stores patient data as high-dimensional vectors (embeddings). When a query is made, Qdrant finds the most mathematically similar records, even if the exact words don't match.
2.  **High-Performance Retrieval:** Optimized for rapid searching across thousands of records, ensuring the Vapi assistant doesn't experience significant delays while "thinking."
3.  **Scalable Data Storage:** Manages the `enterprise_kb` collection, which contains the processed summaries of the Tribal Mental Health Survey.

### The Data Pipeline:
- **Embedding:** Raw CSV data is transformed into natural language strings and then converted into 768-dimensional vectors using Google Vertex AI's `text-embedding-004` model.
- **Indexing:** These vectors are indexed in Qdrant using **Cosine Similarity**, allowing for nuanced retrieval of clinical themes like "Supernatural Beliefs" or "First Contact History."

---

## 🛠️ Combined Workflow
1.  **User Speaks:** "Tell me about beliefs in witchcraft among the patients."
2.  **Vapi:** Transcribes the audio and identifies a need for data retrieval.
3.  **FastAPI Bridge:** Receives the request, generates an embedding for the query, and asks **Qdrant** for relevant matches.
4.  **Qdrant:** Returns the top clinical summaries related to "witchcraft."
5.  **Vapi:** Reads the summaries, synthesizes a concise answer, and speaks it back to the user.
