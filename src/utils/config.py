"""
Configuration management for the LinkedIn Post Generator.
Handles environment variables and API keys.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if not in Docker
if not os.getenv("DOCKER_CONTAINER"):
    load_dotenv()

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")