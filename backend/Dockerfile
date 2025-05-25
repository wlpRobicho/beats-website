# Use official Python base image
FROM python:3.11-slim

# Avoid interactive prompts during installs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv or virtualenv (optional)
# RUN pip install pipenv

# Install Python dependencies (only re-run if requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code into container
COPY . .

# Create logs folder (avoid runtime issues)
RUN mkdir -p /app/logs

# Expose port 8000
EXPOSE 8000

# Run the app (dev server for now — use gunicorn for prod)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
