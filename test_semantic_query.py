import requests
import json

# Your local FastAPI server
URL = "http://localhost:8000/vapi-webhook"

# Mock payload that Vapi sends to your webhook
# It usually contains the transcript of what the user said
payload = {
    "message": {
        "type": "transcript",
        "transcriptType": "final",
        "transcript": "What are the common beliefs about witchcraft in the Munda tribe according to our patient records?",
        "role": "user"
    }
}

print(f"--- Sending Mock Vapi Request to {URL} ---")
print(f"User Question: {payload['message']['transcript']}")

try:
    response = requests.post(URL, json=payload, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ API Response:")
        print(json.dumps(data, indent=2))
        
        # Check if the response actually contains information from our data
        if "response" in data:
            print("\n--- AI Assistant says: ---")
            print(data["response"])
    else:
        print(f"\n❌ Error: Received status code {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"\n❌ Connection Failed: {e}")
    print("\nTip: Ensure your FastAPI server is running (python -m uvicorn app.main:app --port 8000)")
