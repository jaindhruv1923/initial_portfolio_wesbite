# Multi-stage production container for KAVACH AI DevOps Security Platform
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (curl for health check, git for AST repo analysis)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
COPY kavach/backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy source code and frontend assets
COPY kavach/backend /app/backend
COPY kavach/frontend /app/frontend

# Ensure persistent directories exist
RUN mkdir -p /app/backend/data /app/backend/qdrant_storage

# Expose HTTP port (Render, Railway, Fly.io, Cloud Run inject $PORT)
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
EXPOSE 8000

# Container liveness check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Launch uvicorn web service
CMD ["sh", "-c", "uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port ${PORT}"]
