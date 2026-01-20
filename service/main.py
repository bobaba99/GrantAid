import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from src.models import (
    Experience, FundingDefinition, RemixedExperienceRequest, 
    RemixedExperienceResponse
)
from src.utils import get_logger, format_error_response
from src.llm_client import LLMClient
from src.remixer import ExperienceRemixer
from src.ranker import ExperienceRanker

logger = get_logger("grantaid-service")

app = FastAPI(title="GrantAid Service")

# Dependencies
def get_llm_client():
    return LLMClient()

def get_remixer(llm=Depends(get_llm_client)):
    return ExperienceRemixer(llm)

def get_ranker(llm=Depends(get_llm_client)):
    return ExperienceRanker(llm)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "GrantAid Backend"}

@app.post("/remix", response_model=RemixedExperienceResponse)
def remix_experience(
    request: RemixedExperienceRequest,
    remixer: ExperienceRemixer = Depends(get_remixer)
):
    """
    Rewrites an experience to match a funding's requirements using LLM.
    """
    try:
        logger.info(f"Remixing experience for funding: {request.target_funding.name}")
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
    ranker: ExperienceRanker = Depends(get_ranker)
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
