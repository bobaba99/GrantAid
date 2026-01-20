import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.models import (
    Experience, FundingDefinition, RemixedExperienceRequest, 
    RemixedExperienceResponse
)
from src.remixer import ExperienceRemixer
from src.ranker import ExperienceRanker
from src.utils import get_logger, format_error_response
from src.dependencies import (
    get_current_user, get_remixer, get_ranker
)
from src.routes import funding

logger = get_logger("grantaid-service")

app = FastAPI(title="GrantAid")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(funding.router, prefix="/api/funding", tags=["funding"])

@app.get("/")
def read_root():
    return {"status": "ok", "service": "GrantAid Backend", "version": "1.0.0"}

@app.get("/me")
def read_current_user(user = Depends(get_current_user)):
    return {"id": user.id, "email": user.email}

@app.post("/remix", response_model=RemixedExperienceResponse)
def remix_experience(
    request: RemixedExperienceRequest,
    remixer: ExperienceRemixer = Depends(get_remixer),
    user = Depends(get_current_user)
):
    """
    Rewrites an experience to match a funding's requirements using LLM.
    """
    try:
        logger.info(f"Remixing experience for funding: {request.target_funding.name} (User: {user.email})")
        return remixer.remix_experience(
            request.experience, 
            request.target_funding
        )
    except Exception as e:
        error = format_error_response(e)
        logger.error(error)
        raise HTTPException(status_code=500, detail=error)

# Ranker
class RankRequest(BaseModel):
    experience: Experience
    target_funding: FundingDefinition

@app.post("/rank")
def rank_experience(
    request: RankRequest,
    ranker: ExperienceRanker = Depends(get_ranker),
    user = Depends(get_current_user)
):
    """
    Scores an experience for a specific funding.
    """
    try:
        result = ranker.rank_experience(request.experience, request.target_funding)
        return result
    except Exception as e:
        error = format_error_response(e)
        raise HTTPException(status_code=500, detail=error)
