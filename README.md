# LinkedIn Post Generator Agent 🤖 [POC]

> **Note**: This project is an educational proof of concept exploring AI-driven content generation and workflow automation using LangGraph and Ollama.

## 📋 Overview

An intelligent agent that transforms plain text into engaging LinkedIn posts through an iterative, feedback-driven approach. Built with LangGraph and Ollama, it demonstrates how AI can simulate a team of content experts working together.

## 📋 Quick Start

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) installed and running
- Required Ollama model: `llama3:latest`

### Installation

```bash
# Clone the repository
git clone [REPO_URL]
cd linkedin-agent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -e .

# Start Ollama service
ollama serve

# Pull required model
ollama pull llama3:latest
```

## 🔌 API Usage

### Start the API

```bash
uvicorn src.api:app --reload
```

The API will be available at http://localhost:8000

### Endpoints

#### Generate Post
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "We are launching a new AI product",
    "target_audience": "Tech leaders",
    "n_drafts": 3
  }'
```

Response:
```json
{
  "final_post": "...",
  "all_versions": [
    {
      "version": 1,
      "content": "...",
      "feedback": null
    }
  ],
  "workflow_status": "completed"
}
```

#### Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-12-27T09:00:00.000Z",
  "version": "1.0.0",
  "environment": {
    "python_version": "3.11.0",
    "platform": "..."
  },
  "services": {
    "ollama": {
      "status": "healthy",
      "model": "llama3:latest",
      "available": true,
      "available_models": ["llama3:latest", "..."]
    }
  },
  "system": {
    "cpu_usage": 45.2,
    "memory": {
      "total": 17179869184,
      "available": 8589934592,
      "percent": 50.0
    },
    "disk": {
      "total": 499963174912,
      "free": 374972680192,
      "percent": 25.0
    }
  }
}
```

## 🐳 Docker Deployment

### Quick Start with Docker

```bash
# Build and start the container
docker-compose up --build

# The API will be available at:
# - API: http://localhost:8000
```

### Environment Variables

```env
DOCKER_CONTAINER=true
OLLAMA_BASE_URL=http://localhost:11434
```

## 🏗 Technical Architecture

### Core Components

1. **API Layer** (`src/api.py`)
   - FastAPI application
   - Health monitoring
   - Request validation

2. **Workflow Engine** (`src/workflow.py`)
   - LangGraph state management
   - Node orchestration
   - Conditional routing

3. **AI Agents** (`src/services/linkedin_agent.py`)
   - Editor: Improves text clarity
   - Writer: Creates LinkedIn-optimized content
   - Critic: Provides feedback
   - Supervisor: Manages iterations

4. **Models** (`src/models/`)
   - State management
   - Post structure
   - Configuration

### Configuration

Key parameters in `src/utils/constants.py`:
```python
OLLAMA_MODEL = "llama3:latest"
OLLAMA_TEMPERATURE = 0.7
MAX_POST_LENGTH = 1300
MIN_HASHTAGS = 3
MAX_HASHTAGS = 5
```

## 📄 License

This project is released under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This is a proof of concept for educational purposes. While it demonstrates interesting possibilities in AI-driven content generation, it should not be considered production-ready software.

## 📚 Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [Ollama Documentation](https://ollama.com/)
- [LinkedIn Content Best Practices](https://members.linkedin.com/create)

