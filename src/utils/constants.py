"""
Constants used throughout the application
"""

import os

# API Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = "llama3:latest"
OLLAMA_TEMPERATURE = 0.7

# Workflow Configuration
DEFAULT_N_DRAFTS = 3

# LinkedIn Post Constraints
MAX_POST_LENGTH = 1300
MIN_HASHTAGS = 3
MAX_HASHTAGS = 5

# Module Names
LOGGER_NAME = "linkedin_agent" 