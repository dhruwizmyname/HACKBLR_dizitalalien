# HackBLR Mental Health Voice Assistant 🎙️

A unified React and Node.js application designed for seamless deployment on Render, providing an AI-driven interface for tribal mental health data.

## 🚀 Features

- **Live Web App:** [https://cautious-space-enigma-7r4vg5wvrrgfx4jr-5173.app.github.dev/](https://cautious-space-enigma-7r4vg5wvrrgfx4jr-5173.app.github.dev/)
- **Voice Interaction:** Leverages Vapi AI for a responsive conversational experience.
- **Semantic Search:** Provides keyword-based search via a local JSON database, with advanced semantic search capabilities through an external Python API and Qdrant Vector DB.
- **Unified Architecture:** A streamlined Node.js backend serves the React frontend, facilitating single-service deployment.

## 📁 Project Structure

```text
├── api/              # Node.js Express server
│   └── server.js     # Backend logic and static file serving
├── data/             # Persistent data storage
│   └── mental_health_db.json
├── src/              # React frontend source code
├── public/           # Static assets
├── dist/             # Production build artifacts (auto-generated)
├── render.yaml       # Deployment configuration blueprint
└── package.json      # Unified project manifest and configuration
```

## 🛠️ Available Scripts

Execute the following commands in the project root:

| Command | Description |
| :--- | :--- |
| `npm run dev` | Launches the Vite development server for the frontend. |
| `npm run backend` | Starts the Node.js API server for local development. |
| `npm run build` | Compiles the React application for production. |
| `npm start` | Executes the production server (serves the API and static frontend). |
| `npm run lint` | Performs static code analysis using ESLint. |
| `npm run preview` | Previews the production build locally. |

## 📦 Deployment on Render

This project is pre-configured for Render using the `render.yaml` blueprint.

1. **Link Repository:** Connect your GitHub repository to a new Render Web Service.
2. **Automatic Configuration:** Render will utilize the blueprint to configure the build and start commands.
3. **Environment Variables:** Configure the following keys in the Render dashboard:
   - `VITE_VAPI_PUBLIC_KEY`: Your Vapi public key.
   - `VITE_VAPI_ASSISTANT_ID`: Your Vapi assistant ID.
   - `PYTHON_API_URL`: (Optional) Endpoint for the semantic search service.

---

# 🏆 HACKBLR Bootcamp Compliance

- **🛠 Mandatory Tech Stack:** This project strictly utilizes both **Qdrant** (Vector Database) and **Vapi** (Voice AI).
- **⚡ MVP Status:** This is a fully functional MVP/project, integrating a unified Node.js/React frontend with a semantic search backend.
- **📅 Evaluation:** Ready for mentor evaluation on **18th April**.

---

# 📓 Data Master Notebook

## 1. Executive Summary
* **Objective:** Develop an AI-driven Voice Assistant (utilizing Vapi.ai) to facilitate the querying and summarization of tribal mental health clinical data.
* **Primary Data Source:** Central Institute of Psychiatry (CIP) - Tribal Populations Mental Health Utilization Survey.
* **Architecture:** CSV → Python (Pandas + Sentence Transformers) → Qdrant Vector DB → FastAPI (Bridge) → Vapi AI.

## 2. Dataset Specification
* **Filename:** `CIP_LATEST.csv`
* **Dataset Size:** 200 Patient Records
* **Dimensionality:** 85 Features
* **Key Clinical Scales:** 
  * **ASS:** Affiliate Stigma Scale (22 items)
  * **ZBA:** Zarit Burden Assessment (12 items)
  * **CAMI:** Community Attitudes toward Mental Illness (11 items)
  * **SAQ:** Supernatural Attitude Questionnaire

## 3. Data Dictionary (Codebook)
*Numerical codes in the source CSV are mapped to descriptive text for enhanced LLM processing.*

### A. Demographics
| Feature | Code | Description |
| :--- | :--- | :--- |
| **Gender** | 1 | Male |
| | 2 | Female |
| | 3 | Transgender |

### B. Clinical History
| Feature | Code | Description |
| :--- | :--- | :--- |
| **First_Contact** | 1 | General Physician |
| | 2 | Psychiatrist |
| | 3 | Homeopathy |
| | 4 | Ayurveda |
| | 7 | Traditional Healer (Ojha/Tantrik) |
| | 11 | Other Traditional Healer |
| **Traditional Remedies** | 1 | Yes |
| | 2 | No |
| **Information Sources** | 1 | Media (TV/FM) |
| | 2 | Online Resources |
| | 8 | Interpersonal (Friend/Family) |

### C. Substance Use Assessment
| Feature | Code | Description |
| :--- | :--- | :--- |
| **Substance Type** | 1 - 4 | Local/Indigenous Brews (Mahua, Tari, Hadiya) |
| | 5 - 10 | Commercial Spirits (Whisky, Rum, Vodka, Beer) |
| | 12 | Cannabis (Ganja/Charas/Bhang) |
| | 15 | Tobacco Products |
| **Usage Frequency** | 1 | Occasional |
| | 2 | Regular |
| | 3 | High Frequency (Multiple times daily) |
| | 5 | Binge Consumption |
| **Motivators** | 1 | Social Conformity |
| | 3 | Stress/Anxiety Management |
| | 4 | Depression/Loneliness |
| | 6 | Pain Management |

### D. Supernatural Attitudes (SAQ)
*Applies to variables such as `SAQ_Witchcraft`, `SAQ_Ghosts`, `SAQ_EvilEye`.*
| Feature | Code | Description |
| :--- | :--- | :--- |
| **All SAQ Variables** | 1 | Affirmative (Yes) |
| | 2 | Negative (No) |

---

## 4. Semantic Integration Logic
Numerical data is transformed into natural language strings prior to embedding in the Qdrant Vector Database to ensure optimal LLM comprehension.

**Sample Transformation:**
* **Original Entry:** `Gender: 1, First_Contact: 7, SAQ_Witchcraft: 1`
* **Semantic Summary:** *"The subject is Male. Initial clinical consultation was sought through a Traditional Healer. The subject attributes psychiatric illness to supernatural causes, specifically witchcraft."*

## 5. Deployment and Technical Specifications
* **Environment:** GitHub Codespaces (FastAPI Bridge Execution).
* **Network Configuration:** Port `8000` (Must be configured as **Public** during verification).
* **Vapi Tool Endpoint:** `https://[CODESPACE-URL]/search_patient`
* **Vapi Tool Identifier:** `search_patient`

## 📄 License
This project is proprietary and intended for HackBLR stakeholders.
