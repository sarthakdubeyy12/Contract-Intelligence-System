FROM python:3.11-slim

WORKDIR /app

# System dependencies (for pdfplumber, PyPDF2, spacy, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy worker code into container
COPY . .

# Default command (can be overridden in docker-compose)
CMD ["celery", "-A", "celery_app.celery_app", "worker", "--loglevel=info", "-Q", "contracts"]