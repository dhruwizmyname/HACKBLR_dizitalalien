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

const DB_PATH = path.join(__dirname, '../data/mental_health_db.json');

// SPIFFE Client Initialization
let spiffeClientInstance = null;
try {
    spiffeClientInstance = new SpiffeWorkloadAPIClient({
        spiffeSocketPath: process.env.SPIFFE_ENDPOINT_SOCKET || '/tmp/spire-agent/public/api.sock'
    });
    console.log("SPIFFE Workload Client initialized:", !!spiffeClientInstance);
} catch (e) {
    console.warn("SPIFFE not available, falling back to insecure communication:", e.message);
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
    console.log(`AI Search Query: ${query} (Semantic: ${useSemantic})`);
    
    if (!query) {
        return res.status(400).json({ error: 'Search query is required' });
    }

    if (useSemantic && PYTHON_API_URL) {
        try {
            console.log("Forwarding to Python Semantic Search...");
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
            console.error("Semantic search failed, falling back to local search:", e.message);
        }
    }

    const db = readDB();
    const results = (db.resources || []).filter(r => 
        r.name?.toLowerCase().includes(query.toLowerCase()) || 
        r.description?.toLowerCase().includes(query.toLowerCase()) ||
        r.category?.toLowerCase().includes(query.toLowerCase())
    );

    const faqs = (db.frequently_asked_questions || []).filter(f => 
        f.question?.toLowerCase().includes(query.toLowerCase()) || 
        f.answer?.toLowerCase().includes(query.toLowerCase())
    );

    res.json({
        found_resources: results,
        found_faqs: faqs,
        context: "Use this data to answer the user's question directly and concisely."
    });
});

app.get('/api/health', (req, res) => {
    res.json({ status: 'Database server is healthy and running' });
});

app.listen(PORT, () => {
    console.log(`Backend Server running on port ${PORT}`);
});
