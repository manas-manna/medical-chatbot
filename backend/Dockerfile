# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

# Create working dir and install build dependencies
WORKDIR /install
COPY requirements.txt .

# Install dependencies into a separate location
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
    && pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /root/.cache /var/lib/apt/lists/*

# ---------- Stage 2: Final Image ----------
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only the installed packages from builder
COPY --from=builder /install /usr/local

# Copy your application code
COPY app/ ./app
COPY ml_models/ ./ml_models
COPY .scispacy/datasets/ /root/.scispacy/datasets/
COPY requirements.txt .

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

