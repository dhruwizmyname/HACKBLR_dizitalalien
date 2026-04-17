#!/bin/bash
set -e

# Write the Google Cloud credentials to a temporary file if provided via environment variable
if [ -n "$GOOGLE_CREDENTIALS_JSON" ]; then
    echo "Creating Google Cloud credentials file from environment variable..."
    echo "$GOOGLE_CREDENTIALS_JSON" > /tmp/gcp-credentials.json
    export GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-credentials.json
fi

# Execute the FastAPI application
exec uvicorn app.main:app --host 0.0.0.0 --port 10000
