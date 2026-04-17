#!/usr/bin/env bash
# Deployment script for Google Cloud Run
set -e

# Configuration (Update these values)
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"

echo "Deploying HackBLR to Project: $PROJECT_ID in Region: $REGION"

# 1. Deploy Python API
echo "--- Deploying Python Semantic Search API ---"
gcloud run deploy hackblr-python-api \
  --source . \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,QDRANT_COLLECTION=enterprise_kb"

# Get the URL for the Python API
PYTHON_API_URL=$(gcloud run services describe hackblr-python-api --region "$REGION" --format 'value(status.url)')
echo "Python API deployed at: $PYTHON_API_URL"

# 2. Deploy Node/React App
echo "--- Deploying Node.js & React Frontend ---"
cd HackBLR
gcloud run deploy hackblr-app \
  --source . \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "PYTHON_API_URL=$PYTHON_API_URL"

# Get the URL for the main application
APP_URL=$(gcloud run services describe hackblr-app --region "$REGION" --format 'value(status.url)')

echo "--------------------------------------------------------"
echo "DEPLOYMENT COMPLETE! 🎉"
echo "Main Application: $APP_URL"
echo "Python API: $PYTHON_API_URL"
echo "--------------------------------------------------------"
echo "NOTE: You still need to configure the following in the Google Cloud Console:"
echo "1. Set QDRANT_URL and QDRANT_API_KEY environment variables in Cloud Run for 'hackblr-python-api'."
echo "2. Set VITE_VAPI_PUBLIC_KEY and VITE_VAPI_ASSISTANT_ID in Cloud Run for 'hackblr-app'."
echo "--------------------------------------------------------"
