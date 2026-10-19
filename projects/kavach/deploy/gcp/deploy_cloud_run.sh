#!/usr/bin/env bash
# ==============================================================================
# KAVACH Google Cloud Run 1-Click Deployment Script (Bash / Cloud Shell)
# ==============================================================================
set -euo pipefail

REGION="${REGION:-asia-south1}"
PROJECT_ID="${1:-$(gcloud config get-value project 2>/dev/null)}"

if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "(unset)" ]; then
    echo "Error: No GCP Project configured. Run: gcloud config set project <PROJECT_ID>" >&2
    exit 1
fi

echo "============================================================"
echo "  Deploying KAVACH to Google Cloud Run ($REGION) in project $PROJECT_ID"
echo "============================================================"

# Enable APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com --project "$PROJECT_ID"

# Build and Deploy via Cloud Build
gcloud builds submit --config deploy/gcp/cloudbuild.yaml --substitutions=_PROJECT_ID="$PROJECT_ID" .

# Print public URL
SERVICE_URL=$(gcloud run services describe kavach-platform --platform managed --region "$REGION" --format "value(status.url)")
echo "Deployment Complete! Public Endpoint: $SERVICE_URL"
