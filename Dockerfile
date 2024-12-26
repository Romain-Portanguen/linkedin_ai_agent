# Base image with Python and Ollama
FROM ollama/ollama:latest as ollama

# Final image
FROM python:3.11-slim

# Copy Ollama binary from ollama image
COPY --from=ollama /usr/bin/ollama /usr/bin/ollama

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Download Ollama model
RUN ollama serve & \
  sleep 5 && \
  ollama pull llama3 && \
  pkill ollama

# Create startup script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose ports
# ------------
# 11434 - Ollama API
# 8000 - FastAPI
# ------------
EXPOSE 11434
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["docker-entrypoint.sh"] 