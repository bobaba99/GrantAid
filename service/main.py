import os
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from src.models import (
    Experience, GrantDefinition, RemixedExperienceRequest, 
    RemixedExperienceResponse, GrantRequirement
)
from src.utils import get_logger, format_error_response
from src.llm_client import LLMClient
from src.remixer import ExperienceRemixer
from src.diff_engine import DiffEngine

logger = get_logger("grantaid-service")

app = FastAPI(title="GrantAid Service")

# Dependencies
def get_llm_client():
    return LLMClient()

def get_remixer(llm=Depends(get_llm_client)):
    return ExperienceRemixer(llm)

def get_diff_engine():
    return DiffEngine()

# Request Models
class DiffRequest(BaseModel):
    old_requirements: List[GrantRequirement]
    new_requirements: List[GrantRequirement]

@app.get("/")
def read_root():
    return {"status": "ok", "service": "GrantAid Backend"}

@app.post("/remix", response_model=RemixedExperienceResponse)
def remix_experience(
    request: RemixedExperienceRequest,
    remixer: ExperienceRemixer = Depends(get_remixer)
):
    """
    Rewrites an experience to match a grant's requirements using LLM.
    """
    try:
        logger.info(f"Remixing experience for grant: {request.target_grant.name}")
        return remixer.remix_experience(
            request.experience, 
            request.target_grant, 
            request.focus_keywords
        )
    except Exception as e:
        error = format_error_response(e)
        raise HTTPException(status_code=500, detail=error)

@app.post("/diff")
def diff_requirements(
    request: DiffRequest,
    engine: DiffEngine = Depends(get_diff_engine)
):
    """
    Compares two sets of grant requirements.
    """
    try:
        return engine.compare_requirements(request.old_requirements, request.new_requirements)
    except Exception as e:
        error = format_error_response(e)
        raise HTTPException(status_code=500, detail=error)

# Ranker
class RankRequest(BaseModel):
    experience: Experience
    target_grant: GrantDefinition

def get_ranker(llm=Depends(get_llm_client)):
    from src.ranker import ExperienceRanker
    return ExperienceRanker(llm)

@app.post("/rank")
def rank_experience(
    request: RankRequest,
    ranker = Depends(get_ranker)
):
    """
    Scores an experience for a specific grant.
    """
    try:
        result = ranker.rank_experience(request.experience, request.target_grant)
        return result
    except Exception as e:
        error = format_error_response(e)
        raise HTTPException(status_code=500, detail=error)
