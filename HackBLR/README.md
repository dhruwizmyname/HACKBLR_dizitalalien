# hackblr-dizitalalien 🎙️

HackBLR Mental Health Voice Assistant - A unified React + Node.js application designed for easy deployment on Render.

## 🚀 Features

- **Voice Interaction:** Powered by Vapi AI for a seamless conversational experience.
- **Semantic Search:** Supports keyword-based search with a local JSON database and optional semantic search via an external Python API.
- **Unified Architecture:** The Node.js backend serves the React frontend, making it a single-service deployment.

## 📁 Project Structure

```text
├── api/              # Node.js Express server
│   └── server.js     # Main backend logic & static file serving
├── data/             # Database storage
│   └── mental_health_db.json
├── src/              # React frontend source code
├── public/           # Static assets for the frontend
├── dist/             # Production build output (auto-generated)
├── render.yaml       # Deployment blueprint for Render
└── package.json      # Unified project configuration
```

## 🛠️ Available Scripts

In the project directory, you can run:

| Command | Description |
| :--- | :--- |
| `npm run dev` | Starts the Vite development server for the frontend. |
| `npm run backend` | Starts the Node.js API server for local development. |
| `npm run build` | Builds the React frontend for production. |
| `npm start` | Runs the production server (serves the API and the built frontend). |
| `npm run lint` | Runs ESLint to check for code quality issues. |
| `npm run preview` | Locally previews the production build. |

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
│   └── App.css / index.css # Styling
├── index.html              # Frontend entry point
├── render.yaml             # Render deployment configuration
├── package.json            # Scripts and dependencies
└── vite.config.js          # Vite configuration
```

### Deployment on Render
This project is pre-configured for Render using the `render.yaml` blueprint.

1. Connect your GitHub repository to Render.
2. Render will automatically detect the blueprint and set up:
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `npm start`
   - **Runtime:** Node.js

### Environment Variables
Ensure the following are set in your deployment environment:
- `VITE_VAPI_PUBLIC_KEY`: Your Vapi public key.
- `VITE_VAPI_ASSISTANT_ID`: Your Vapi assistant ID.
- `PYTHON_API_URL`: (Optional) URL for the semantic search backend.

## 📄 License
This project is private and intended for HackBLR.
