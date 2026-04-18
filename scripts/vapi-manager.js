import fetch from 'node-fetch';
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';

dotenv.config();

const VAPI_SECRET_KEY = process.env.VAPI_SECRET_KEY;
const ASSISTANT_ID = process.env.VITE_VAPI_ASSISTANT_ID;

if (!VAPI_SECRET_KEY) {
    console.error('Error: VAPI_SECRET_KEY is not defined in your .env file.');
    process.exit(1);
}

const args = process.argv.slice(2);
const command = args[0];

const getAssistant = async () => {
    const response = await fetch(`https://api.vapi.ai/assistant/${ASSISTANT_ID}`, {
        headers: { 'Authorization': `Bearer ${VAPI_SECRET_KEY}` }
    });
    return await response.json();
};

const updateAssistant = async (data) => {
    const response = await fetch(`https://api.vapi.ai/assistant/${ASSISTANT_ID}`, {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ${VAPI_SECRET_KEY}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return await response.json();
};

async function main() {
    switch (command) {
        case 'get':
            console.log('Fetching assistant configuration...');
            const config = await getAssistant();
            fs.writeFileSync('vapi-assistant.json', JSON.stringify(config, null, 2));
            console.log('Saved to vapi-assistant.json');
            break;
            
        case 'push':
            console.log('Updating assistant from vapi-assistant.json...');
            const newConfig = JSON.parse(fs.readFileSync('vapi-assistant.json', 'utf8'));
            // Remove read-only fields
            delete newConfig.id;
            delete newConfig.orgId;
            delete newConfig.createdAt;
            delete newConfig.updatedAt;
            
            const result = await updateAssistant(newConfig);
            console.log('Update successful:', result);
            break;

        default:
            console.log('Usage:');
            console.log('  node scripts/vapi-manager.js get  - Downloads config to vapi-assistant.json');
            console.log('  node scripts/vapi-manager.js push - Uploads config from vapi-assistant.json');
    }
}

main().catch(console.error);
