#!/bin/bash
set -e

# Start Ollama in background
ollama serve &

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
until curl -s http://localhost:11434/api/tags >/dev/null; do
    sleep 1
done
echo "Ollama is ready!"

# Start FastAPI application
exec uvicorn src.api:app --host 0.0.0.0 --port 8000 