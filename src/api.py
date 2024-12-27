from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import platform
import psutil
import ollama
from src.main import generate_linkedin_post
from src.utils.constants import OLLAMA_MODEL

app = FastAPI(
    title="LinkedIn Post Generator API",
    description="Generate optimized LinkedIn posts using AI",
    version="1.0.0"
)

class PostRequest(BaseModel):
    text: str
    target_audience: str
    n_drafts: Optional[int] = 3

class PostResponse(BaseModel):
    final_post: str
    all_versions: list[dict]
    workflow_status: str

class HealthResponse(BaseModel):
    """Detailed health check response"""
    status: str
    timestamp: str
    version: str
    environment: Dict[str, str]
    services: Dict[str, Dict[str, Any]]
    system: Dict[str, Any]

@app.post("/generate", response_model=PostResponse)
async def generate_post(request: PostRequest) -> PostResponse:
    """Generate an optimized LinkedIn post"""
    try:
        result = generate_linkedin_post(
            text=request.text,
            target_audience=request.target_audience,
            n_drafts=request.n_drafts
        )
        if result is None:
            raise HTTPException(status_code=500, detail="Failed to generate post")
        return PostResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check() -> HealthResponse:
    """
    Comprehensive health check endpoint
    
    Returns:
        Detailed health status of the API and its dependencies
    """
    try:
        ollama_status = "healthy"
        ollama_details = {"model": OLLAMA_MODEL, "available": True}
        model_names = []
        
        try:
            models = ollama.list()
            model_names = [model.get('model') for model in models.get('models', [])]
            if OLLAMA_MODEL not in model_names:
                ollama_status = "degraded"
                ollama_details.update({
                    "available": False,
                    "error": f"Model {OLLAMA_MODEL} not found in available models: {model_names}"
                })
        except Exception as e:
            ollama_status = "degraded"
            ollama_details.update({
                "available": False,
                "error": str(e)
            })

        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow().isoformat(),
            version="1.0.0",
            environment={
                "python_version": platform.python_version(),
                "platform": platform.platform(),
            },
            services={
                "ollama": {
                    "status": ollama_status,
                    **ollama_details,
                    "available_models": model_names if ollama_status == "healthy" else []
                }
            },
            system={
                "cpu_usage": psutil.cpu_percent(interval=1),
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent
                },
                "disk": {
                    "total": disk.total,
                    "free": disk.free,
                    "percent": disk.percent
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service health check failed: {str(e)}"
        ) 