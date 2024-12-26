"""
FastAPI application for the LinkedIn Post Generator.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from .main import generate_linkedin_post

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

@app.post("/generate", response_model=PostResponse)
async def generate_post(request: PostRequest) -> PostResponse:
    """Generate an optimized LinkedIn post"""
    try:
        result = generate_linkedin_post(
            text=request.text,
            target_audience=request.target_audience,
            n_drafts=request.n_drafts
        )
        return PostResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 