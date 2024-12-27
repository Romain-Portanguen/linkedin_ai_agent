# Base image with Python and Ollama
FROM ollama/ollama:latest as ollama

# Final image
FROM python:3.11-slim

# Copy Ollama binary from ollama image
COPY --from=ollama /usr/bin/ollama /usr/bin/ollama

# Set working directory
WORKDIR /app

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
  curl \
  && rm -rf /var/lib/apt/lists/* \
  && curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy only dependency files first
COPY pyproject.toml .

# Install dependencies with uv
RUN uv pip sync pyproject.toml

# Copy rest of the project files
COPY . .

# Download Ollama model
RUN ollama serve & \
  sleep 5 && \
  ollama pull llama3:latest && \
  pkill ollama

# Create startup script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose ports
# 11434 - Ollama API
EXPOSE 11434
# 8000 - FastAPI
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["docker-entrypoint.sh"] 