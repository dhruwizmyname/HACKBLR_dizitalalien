
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
| :--- | :--- | :--- |
| **Gender** | 1 | Male |
| | 2 | Female |
| | 3 | Transgender |

### B. Clinical History
| Variable | Code | Meaning |
| :--- | :--- | :--- |
| **First_Contact** | 1 | General Physician |
| | 2 | Psychiatrist |
| | 3 | Homeopathy |
| | 4 | Ayurveda |
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
