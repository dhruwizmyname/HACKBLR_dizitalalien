#!/usr/bin/env bash
# Script to set up Qdrant on Google Compute Engine
set -e

PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
ZONE="us-central1-a"
INSTANCE_NAME="hackblr-qdrant-db"

echo "Step 1: Creating Firewall Rule to allow Qdrant traffic (Port 6333)..."
gcloud compute firewall-rules create allow-qdrant \
    --allow tcp:6333 \
    --description="Allow Qdrant API traffic" \
    --direction=INGRESS \
    --priority=1000 \
    --network=default || echo "Firewall rule already exists."

echo "Step 2: Launching Qdrant VM Instance..."
# This uses a small, cost-effective machine (e2-small)
gcloud compute instances create-with-container $INSTANCE_NAME \
    --container-image=qdrant/qdrant \
    --container-mount-host-path=host-path=/mnt/stateful_partition/qdrant,mount-path=/qdrant/storage \
    --machine-type=e2-small \
    --zone=$ZONE \
    --tags=http-server \
    --labels=app=hackblr

echo "Step 3: Fetching your Qdrant External IP..."
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "--------------------------------------------------------"
echo "QDRANT SETUP SUCCESSFUL! 🎉"
echo "Your Qdrant URL is: http://$EXTERNAL_IP:6333"
echo "--------------------------------------------------------"
echo "Next Steps:"
echo "1. Run your Data_Injector.py with this new URL to upload your data."
echo "2. Use this URL in your Cloud Run 'QDRANT_URL' environment variable."
echo "--------------------------------------------------------"
