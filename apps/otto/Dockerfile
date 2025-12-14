# Dockerfile for Otto API Service
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Note: Replace uvicorn[standard] with uvicorn to avoid Rust dependency
RUN sed 's/uvicorn\[standard\]/uvicorn/g' requirements.txt > requirements_clean.txt && \
    pip install --no-cache-dir -r requirements_clean.txt

# Copy Otto application code
COPY otto/ ./otto/
COPY otto_config.yaml .

# Expose port (Railway/Fly.io will override with PORT env var)
EXPOSE 8001

# Health check (uses fixed port - platform will map correctly)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; import os; port = int(os.getenv('PORT', 8001)); httpx.get(f'http://localhost:{port}/health', timeout=5)"

# Start command - use PORT env var if available, default to 8001
ENV PORT=8001
CMD python -c "import os; port = int(os.getenv('PORT', 8001)); import uvicorn; uvicorn.run('otto.api:app', host='0.0.0.0', port=port)"
