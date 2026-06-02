## Parent image
FROM python:3.10-slim

## Essential Environment variables (Real-Time Logging)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED = 1        

## Set working directory inside the container
WORKDIR /app

## Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copy the project files into the container
COPY . .

## Install dependencies
RUN pip install --no-cache-dir -e .

## Expose ports (Frontend - 8501 & Backend - 9999)
EXPOSE 8501
EXPOSE 9999

## Run the application
CMD ["python", "app/main.py"]