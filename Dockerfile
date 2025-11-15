# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (collectstatic doesn't need database, but needs SECRET_KEY)
# Set a temporary SECRET_KEY for build time
ENV SECRET_KEY=temp-secret-key-for-build-only
RUN python manage.py collectstatic --noinput

# Expose port (Cloud Run uses PORT env variable)
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:$PORT/health/')"

# Run Gunicorn
CMD exec gunicorn her_beauty_hub.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 60 --max-requests 1000 --max-requests-jitter 50

