# Data Master Notebook

## 1. Project Overview
* **Objective:** To build an AI-powered Voice Assistant (using Vapi.ai) that can query and summarize tribal mental health clinical data.
* **Source Data:** Central Institute of Psychiatry (CIP) - Tribal Populations Mental Health Utilization Survey.
* **Database Pipeline:** CSV → Python (Pandas + Sentence Transformers) → Qdrant Vector DB → FastAPI (Bridge) → Vapi AI.

## 2. Raw Dataset Details
* **File Name:** `CIP_LATEST.csv`
* **Total Records:** 200 Patients
* **Total Variables:** 85 Columns
* **Key Scales Included:** 
  * ASS (Affiliate Stigma Scale) - 22 items
  * ZBA (Zarit Burden Assessment) - 12 items
  * CAMI (Community Attitudes toward Mental Illness) - 11 items
  * SAQ (Supernatural Attitude Questionnaire)

## 3. The Data Dictionary (Codebook)
*Note: This mapping translates numerical codes in the source CSV into descriptive text for enhanced LLM processing.*

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
| | 7 | Traditional Healer (Ojha/Tantrik) |
| | 11 | Other Traditional Healer |
| **Traditional_remedies** | 1 | Yes |
| | 2 | No |
| **Information_Sources** | 1 | Media (TV/FM) |
| | 2 | Online |
| | 8 | Interpersonal (Friend, Family Member) |

### C. Substance Use Assessment
| Variable | Code | Meaning |
| :--- | :--- | :--- |
| **Substance_Used** | 1 - 4 | Local/Indigenous Brews (Mahua, Tari, Hadiya) |
| | 5 - 10 | Commercial/Foreign Spirits (Whisky, Rum, Vodka, Beer) |
| | 12 | Cannabis (Ganja/Charas/Bhang) |
| | 15 | Tobacco Products (Bidi/Cigarette/Khaini/Gutkha) |
| **Usage_Frequency** | 1 | Occasional |
| | 2 | Regular |
| | 3 | High Frequency (Multiple times daily) |
| | 5 | Binge Consumption |
| **Reason_for_Intoxicant**| 1 | Social Conformity/Pressure |
| | 3 | Stress/Anxiety Management |
| | 4 | Depression/Loneliness |
| | 6 | Pain Management |

### D. SAQ (Supernatural Attitudes)
*Applies to variables such as `SAQ_Witchcraft`, `SAQ_Ghosts`, `SAQ_EvilEye`.*
| Variable | Code | Meaning |
| :--- | :--- | :--- |
| **All SAQ Variables** | 1 | Affirmative (Yes) |
| | 2 | Negative (No) |

---

## 4. Vector Injection Logic (Data Transformation)
To ensure the Vapi AI processes the data naturally, numerical codes are mapped to descriptive strings prior to embedding in the Qdrant Vector Database.

**Example Transformation:**
* **Raw Entry:** `Gender: 1, First_Contact: 7, SAQ_Witchcraft: 1`
* **Semantic Summary (Injected to Qdrant):** *"The patient is Male. Their initial contact for treatment was a Traditional Healer (Ojha/Tantrik). They attribute the cause of illness to supernatural factors, specifically witchcraft."*

## 5. Technical Stack & Deployment Specifications
* **Environment:** GitHub Codespaces (Executing FastAPI Bridge).
* **Network Configuration:** Port `8000` (Must be configured as **Public** during verification).
* **Vapi Tool Endpoint:** `https://[CODESPACE-URL]/search_patient`
* **Vapi Tool Identifier:** `search_patient`

---
*This document serves as the single source of truth for data mapping and system logic.*
