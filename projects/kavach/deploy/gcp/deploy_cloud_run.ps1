# ==============================================================================
# KAVACH Google Cloud Run 1-Click Deployment Script
# Provisions serverless Google ADK runtime in asia-south1 (Mumbai)
# ==============================================================================

param(
    [string]$ProjectId = "",
    [string]$Region = "asia-south1"
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  KAVACH AGENTIC AI: GOOGLE CLOUD RUN ENTERPRISE DEPLOY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Check if gcloud CLI is installed
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Google Cloud SDK (gcloud) is not found in PATH." -ForegroundColor Red
    Write-Host "Please install it from https://cloud.google.com/sdk/docs/install or run in Google Cloud Shell." -ForegroundColor Yellow
    exit 1
}

# 2. Get active project if not supplied
if ([string]::IsNullOrWhiteSpace($ProjectId)) {
    $ProjectId = (gcloud config get-value project 2>$null).Trim()
}

if ([string]::IsNullOrWhiteSpace($ProjectId) -or $ProjectId -eq "(unset)") {
    Write-Host "[ERROR] No GCP Project ID configured. Run: gcloud config set project <PROJECT_ID>" -ForegroundColor Red
    exit 1
}

Write-Host "[INFO] Active GCP Project : $ProjectId" -ForegroundColor Green
Write-Host "[INFO] Deployment Region  : $Region (Mumbai, India)" -ForegroundColor Green

# 3. Enable Required Google Cloud APIs
Write-Host "[1/4] Enabling Cloud Run and Cloud Build APIs..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com --project $ProjectId

# 4. Submit Build via Google Cloud Build
Write-Host "[2/4] Submitting container build to Google Cloud Build..." -ForegroundColor Yellow
gcloud builds submit --config deploy/gcp/cloudbuild.yaml --substitutions=_PROJECT_ID=$ProjectId .

# 5. Retrieve Public Cloud Run URL
Write-Host "[3/4] Retrieving Cloud Run Service URL..." -ForegroundColor Yellow
$ServiceUrl = (gcloud run services describe kavach-platform --platform managed --region $Region --format "value(status.url)").Trim()

Write-Host "============================================================" -ForegroundColor Green
Write-Host "  KAVACH DEPLOYED SUCCESSFULLY TO GOOGLE CLOUD RUN!" -ForegroundColor Green
Write-Host "  Live Public Endpoint: $ServiceUrl" -ForegroundColor Cyan
Write-Host "  Swagger API Docs    : $ServiceUrl/docs" -ForegroundColor Cyan
Write-Host "  Course Cockpit UI   : $ServiceUrl/cockpit" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Green
