## 🚀 Codespace Setup & Installation Guide

We have automated the environment setup process. When launching this project locally or in a GitHub Codespace, follow these steps to initialize your dependencies and local database.


**├── scripts/
│   ├── setup_codespace.sh   # Automated setup for Linux/Mac
│   └── setup_codespace.bat  # Automated setup for Windows
├── qdrant_storage/          # Persistent Qdrant volume (Ignored by Git)
├── core_integration.py      # Phase 1: Qdrant read/write testing script
├── requirements.txt         # Python package dependencies
├── .gitignore               # Standard ignore file for venv, cache, and env vars
└── README.md                # Project documentation**

### Prerequisites 
* **Docker:** Pre-installed in GitHub Codespaces. Ensure Docker Desktop is running if you are working locally.
* **GitHub CLI (`gh`):** Pre-installed in GitHub Codespaces.

---

### Step 1: Run the Automated Setup Script
Instead of manually installing dependencies, run our idempotent setup script. It will intelligently check your environment and only install or start what is missing.

**For Mac/Linux/Codespaces:**
```bash
chmod +x scripts/setup_codespace.sh
./scripts/setup_codespace.sh
```

**For windows:**
DOS
```
scripts\setup_codespace.bat
```

** 🛠 Troubleshooting & Manual Fallback **

Docker: "Port is already allocated" or "Bind for 0.0.0.0:6333 failed"
If you try to run the setup and get a port allocation error, a previous container or ghost process is likely occupying the port. Clear all running containers with:

** Docker: "Port is already allocated" or "Bind for 0.0.0.0:6333 failed" **

If you try to run the setup and get a port allocation error, a previous container or ghost process is likely occupying the port. Clear all running containers with:

** BASH **
```
docker rm -f $(docker ps -aq)

```
** Manual Qdrant Start **

Docker: "Port is already allocated" or "Bind for 0.0.0.0:6333 failed"
If you try to run the setup and get a port allocation error, a previous container or ghost process is likely occupying the port. Clear all running containers with:

** Docker: "Port is already allocated" or "Bind for 0.0.0.0:6333 failed" **

If you try to run the setup and get a port allocation error, a previous container or ghost process is likely occupying the port. Clear all running containers with:

** BASH **
```
docker run -d \
  --name hackblr-qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant

```



