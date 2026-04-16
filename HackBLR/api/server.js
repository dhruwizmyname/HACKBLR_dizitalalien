/* global process, fetch */
import express from 'express';
import cors from 'cors';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { SpiffeWorkloadAPIClient } from 'spiffe';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3001;
const PYTHON_API_URL = process.env.PYTHON_API_URL;

app.use(cors());
app.use(express.json());

// Log all incoming requests for debugging on Render
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

const DB_PATH = path.join(__dirname, '../data/mental_health_db.json');
const DIST_PATH = path.join(__dirname, '../dist');

// Serve static files from the 'dist' directory (production)
app.use(express.static(DIST_PATH));

// Root Route - serves the API status if requested via JSON, else the frontend will be served by static/catch-all
app.get('/api', (req, res) => {
    res.json({ 
        message: 'HackBLR Node.js API is running',
        endpoints: {
            health: '/api/health',
            search: '/api/search (POST)'
        }
    });
});

// SPIFFE Client Initialization
let spiffeClientInstance = null;
try {
    spiffeClientInstance = new SpiffeWorkloadAPIClient({
        spiffeSocketPath: process.env.SPIFFE_ENDPOINT_SOCKET || '/tmp/spire-agent/public/api.sock'
    });
    console.log("SPIFFE Workload Client initialized");
} catch (e) {
    console.warn("SPIFFE not available, falling back to insecure communication");
}

const readDB = () => {
    try {
        const data = fs.readFileSync(DB_PATH, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error("Error reading database file:", error);
        return { resources: [], frequently_asked_questions: [] };
    }
};

app.post('/api/search', async (req, res) => {
    const { query, useSemantic = false } = req.body;
    
    if (!query) {
        return res.status(400).json({ error: 'Search query is required' });
    }

    if (useSemantic && PYTHON_API_URL) {
        try {
            const response = await fetch(PYTHON_API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            const data = await response.json();
            return res.json({
                semantic_results: data.response,
                context: "Semantic search results from Vector DB."
            });
        } catch (e) {
            console.error("Semantic search failed:", e.message);
            // Fallback to keyword search on error
        }
    } else if (useSemantic && !PYTHON_API_URL) {
        console.warn("Semantic search requested but PYTHON_API_URL is not set.");
    }

    const db = readDB();
    const results = (db.resources || []).filter(r => 
        r.name?.toLowerCase().includes(query.toLowerCase()) || 
        r.description?.toLowerCase().includes(query.toLowerCase())
    );

    const faqs = (db.frequently_asked_questions || []).filter(f => 
        f.question?.toLowerCase().includes(query.toLowerCase()) || 
        f.answer?.toLowerCase().includes(query.toLowerCase())
    );

    res.json({
        found_resources: results,
        found_faqs: faqs
    });
});

app.get('/api/health', (req, res) => {
    res.json({ status: 'Database server is healthy and running' });
});

// Use middleware for catch-all to handle Express 5 routing changes
app.use((req, res, next) => {
    // If it's an API request that wasn't handled, send 404
    if (req.path.startsWith('/api')) {
        return res.status(404).json({ error: 'API endpoint not found' });
    }
    
    // Otherwise, serve index.html from dist
    const indexPath = path.join(DIST_PATH, 'index.html');
    if (fs.existsSync(indexPath)) {
        res.sendFile(indexPath);
    } else {
        res.status(404).send('Not Found');
    }
});

app.listen(PORT, () => {
    console.log(`Backend Server running on port ${PORT}`);
});
