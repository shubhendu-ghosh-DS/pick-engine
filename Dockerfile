# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Expose the required port
EXPOSE 7860

# FastAPI (using uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]

