# Use a slim Python image for a smaller footprint
FROM python:3.10-slim

# Set environment variables to optimize Python execution and configure HF Cache
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/data/hf_cache

# Create the cache directory and ensure it is writable
RUN mkdir -p $HF_HOME && chmod 777 $HF_HOME

# Set the working directory to the service root inside the container
WORKDIR /app/ml-service

# Copy requirements first to leverage Docker layer caching
COPY ml-service/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ml-service/app ./app

# Copy the scrapers module from the project root to the container root
# We place it at /app/scrapers because the code does sys.path.append(project_root)
# which resolves to /app when running from /app/ml-service/app
COPY scrapers /app/scrapers

# Expose the port uvicorn will run on
EXPOSE 8000

# Health check using Python (avoids installing curl)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
# We run from /app/ml-service, so 'app.main:app' refers to app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
