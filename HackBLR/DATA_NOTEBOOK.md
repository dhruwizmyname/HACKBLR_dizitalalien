<<<<<<< HEAD
# hackblr-dizitalalien 🎙️

HackBLR Mental Health Voice Assistant - A unified React + Node.js application designed for seamless deployment on Render.

## 🚀 Features

- **Voice Interaction:** Leverages Vapi AI for a responsive conversational experience.
- **Semantic Search:** Provides keyword-based search via a local JSON database, with optional semantic search capabilities through an external Python API.
- **Unified Architecture:** A streamlined Node.js backend that serves the React frontend, facilitating single-service deployment.

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

## 📁 Project Overview

```text
.
├── api/
│   └── server.js           # Express server (API & Static Serving)
├── data/
│   └── mental_health_db.json # Local JSON database
├── public/                 # Static assets (icons, favicons)
├── src/
│   ├── assets/             # Images and SVG assets
│   ├── App.jsx             # Main React component (Vapi integration)
│   ├── main.jsx            # React entry point
│   └── App.css / index.css # Application styling
├── index.html              # Frontend entry point
├── render.yaml             # Render deployment configuration
├── package.json            # Scripts and dependencies
└── vite.config.js          # Vite configuration
```

## 📦 Deployment on Render

This project is pre-configured for Render using the `render.yaml` blueprint.

1. **Link Repository:** Connect your GitHub repository to a new Render Web Service.
2. **Automatic Configuration:** Render will utilize the blueprint to configure:
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `npm start`
   - **Runtime:** Node.js

### Environment Variables
Configure the following keys in the Render dashboard:
- `VITE_VAPI_PUBLIC_KEY`: Your Vapi public key.
- `VITE_VAPI_ASSISTANT_ID`: Your Vapi assistant ID.
- `PYTHON_API_URL`: (Optional) The endpoint for the semantic search service.

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
=======
Bhai, ye sabse professional approach hai! Kisi bhi Data Science ya AI project mein ek "Single Source of Truth" (ek master document) hona bahut zaroori hai taaki jab judges puchen ya tum khud bhool jao, toh ek jagah sab likha ho.

Kyunki main ek AI chat interface hoon, main directly tumhare system mein koi "Notebook file" (jaise Jupyter ya Notion) create aur save nahi kar sakta. Lekin, main yahan ek **Master Markdown Notebook** ka structure bana raha hoon jisme hamara ab tak ka saara raw data logic, codebook, aur updates recorded hain. 

Tum is poore content ko copy karke apne **Notion, Google Docs, ya GitHub ke `README.md`** mein paste kar sakte ho. Yeh tumhari project diary ban jayegi!

---

## 1. Project Overview
* **Objective:** To build an AI-powered Voice Assistant (using Vapi.ai) that can query and summarize tribal mental health clinical data.
* **Source Data:** Central Institute of Psychiatry (CIP) - Tribal Populations Mental Health Utilization Survey.
* **Database Pipeline:** CSV → Python (Pandas + Sentence Transformers) → Qdrant Vector DB → FastAPI (Bridge) → Vapi AI.

## 2. Raw Dataset Details
* **File Name:** `CIP_LATEST.csv`
* **Total Records:** 200 Patients
* **Total Variables:** 85 Columns
* **Key Scales Included:** * ASS (Affiliate Stigma Scale) - 22 items
  * ZBA (Zarit Burden Assessment) - 12 items
  * CAMI (Community Attitudes toward Mental Illness) - 11 items
  * SAQ (Supernatural Attitude Questionnaire)

## 3. The Data Dictionary (Codebook)
*Note: This mapping translates the numerical codes in the CSV into readable text for the LLM.*

### A. Demographics
| Variable | Code | Meaning |
>>>>>>> Dhruw-Shekhar
| :--- | :--- | :--- |
| **Gender** | 1 | Male |
| | 2 | Female |
| | 3 | Transgender |

### B. Clinical History
<<<<<<< HEAD
| Feature | Code | Description |
=======
| Variable | Code | Meaning |
>>>>>>> Dhruw-Shekhar
| :--- | :--- | :--- |
| **First_Contact** | 1 | General Physician |
| | 2 | Psychiatrist |
| | 3 | Homeopathy |
| | 4 | Ayurveda |
<<<<<<< HEAD
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
| **Substance Type** | 1 - 4 | Local Brews (Mahua, Tari, Hadiya) |
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
* **Semantic Summary:** *"The subject is Male. Initial clinical consultation was sought through a Traditional Healer (Ojha/Tantrik). The subject attributes psychiatric illness to supernatural causes, specifically witchcraft."*

## 5. Deployment and Technical Specifications
* **Environment:** GitHub Codespaces (FastAPI Bridge Execution).
* **Network Configuration:** Port `8000` (Must be configured as **Public** during verification).
* **Vapi Tool Endpoint:** `https://[CODESPACE-URL]/search_patient`
* **Vapi Tool Identifier:** `search_patient`

## 📄 License
This project is proprietary and intended for HackBLR stakeholders.
=======
| | 7 | Ojha/Tantrik |
| | 11 | Traditional Healer |
| **Traditional_remedies** | 1 | Yes |
| | 2 | No |
| **Information_Sources** | 1 | TV/FM |
| | 2 | Online |
| | 8 | Friend, Family Member |

### C. Substance Use Assessment
| Variable | Code | Meaning |
| :--- | :--- | :--- |
| **Substance_Used** | 1 - 4 | Desi (Mahua, Tari, Hadiya) |
| | 5 - 10 | Foreign (Whisky, Rum, Vodka, Beer) |
| | 12 | Ganja/Charas/Bhang |
| | 15 | Tobacco (Bidi/Cigarette/Khaini/Gutkha) |
| **Usage_Frequency** | 1 | Occasionally |
| | 2 | Regularly |
| | 3 | Multiple times a day |
| | 5 | Binge drinking (Atyadhik matra) |
| **Reason_for_Intoxicant**| 1 | Social pressure |
| | 3 | Stress/Anxiety |
| | 4 | Depression/Loneliness |
| | 6 | Pain relief |

### D. SAQ (Supernatural Attitudes)
*Applies to variables like `SAQ_Witchcraft`, `SAQ_Ghosts`, `SAQ_EvilEye`*
| Variable | Code | Meaning |
| :--- | :--- | :--- |
| **All SAQ Variables** | 1 | Yes (Haan) |
| | 2 | No (Na) |

---

## 4. Vector Injection Logic (Data Transformation)
To ensure the Vapi AI reads the data naturally, the numerical codes are mapped to text strings before being embedded into the Qdrant Database.

**Example Transformation:**
* **Raw Row:** `Gender: 1, First_Contact: 7, SAQ_Witchcraft: 1`
* **Semantic Summary (Injected to Qdrant):** *"The patient is Male. Their first contact for treatment was an Ojha/Tantrik. They believe witchcraft is a cause of illness (Yes)."*

## 5. Technical Stack & Deployment State
* **Codespace:** GitHub Codespaces (Running FastAPI Bridge).
* **Port:** `8000` (Must be set to **Public** during testing).
* **Vapi Tool Endpoint:** `https://[YOUR-CODESPACE-URL]/search_patient`
* **Vapi Tool Name:** `search_patient`

---

### How to use this:
Bhai, is upar wale text ko copy kar lo aur ek file bana lo `DATA_NOTEBOOK.md` apne Codespace mein. Aage jo bhi naya variable ya update aayega, hum isme add karte jayenge!
>>>>>>> Dhruw-Shekhar
