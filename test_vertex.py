import vertexai
from vertexai.generative_models import GenerativeModel
import os
from dotenv import load_dotenv

# Load .env to get GOOGLE_APPLICATION_CREDENTIALS if set
load_dotenv()

try:
    vertexai.init(project="hackblr-493411", location="us-central1")
    model = GenerativeModel("gemini-1.5-pro")
    print("Connecting to Vertex AI...")
    response = model.generate_content("Plan a MVP for HackBLR")
    print("\n--- Response from Gemini ---\n")
    print(response.text)
except Exception as e:
    print(f"\nError: {e}")
    print("\nTip: Make sure GOOGLE_APPLICATION_CREDENTIALS is set correctly in your .env file and the path is valid.")
