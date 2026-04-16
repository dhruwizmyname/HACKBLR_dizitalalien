import express from 'express';
import cors from 'cors';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Path to JSON DB (one level up from /api folder)
const DB_PATH = path.join(__dirname, '../data/mental_health_db.json');

// Helper to read DB
const readDB = () => {
    try {
        const data = fs.readFileSync(DB_PATH, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error("Error reading database file:", error);
        return { resources: [], frequently_asked_questions: [] };
    }
};

// Vapi "Tool" Endpoint: Search the database
app.post('/api/search', (req, res) => {
    const { query } = req.body;
    console.log(`AI Search Query: ${query}`);
    
    if (!query) {
        return res.status(400).json({ error: 'Search query is required' });
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
