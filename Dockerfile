# syntax=docker/dockerfile:1
FROM python:3.10-slim

# Install system dependencies required by WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libffi-dev \
    libxml2 \
    libxslt1.1 \
    shared-mime-info \
    fonts-liberation \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source and examples
COPY ./src ./src
COPY ./examples ./examples

# Add src to PYTHONPATH to make imports work
ENV PYTHONPATH=/app/src

# Optional: expose volume if needed for PDFs
VOLUME ["/app/output"]

# Default run command
CMD ["python", "examples/render_example.py"]
