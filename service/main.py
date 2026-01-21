import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.models import (
    Experience, FundingDefinition, StoryTellingRequest, 
    StoryTellingResponse
)
from src.story_teller import StoryTeller
from src.utils import get_logger, format_error_response
from src.dependencies import (
    get_current_user, get_story_teller, supabase
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
from src.routes import experiences
app.include_router(experiences.router, prefix="/api", tags=["experiences"])

@app.get("/")
def read_root():
    return {"status": "ok", "service": "GrantAid Backend", "version": "1.0.0"}

@app.get("/me")
def read_current_user(user = Depends(get_current_user)):
    try:
        # Check 'profiles' table for additional info
        profile_response = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
        profile_data = profile_response.data if profile_response.data else {}
    except Exception as e:
        logger.warning(f"Could not fetch profile for {user.id}: {e}")
        profile_data = {}

    # Merge auth email (authoritative) with profile data
    return {
        "id": user.id, 
        "email": user.email,
        "full_name": profile_data.get("full_name", ""),
        "program_level": profile_data.get("program_level", ""),
        "research_field": profile_data.get("research_field", ""),
        "research_focus": profile_data.get("research_focus", ""),
        "institution": profile_data.get("institution", "")
    }


@app.post("/story-tell", response_model=StoryTellingResponse)
def tell_story(
    request: StoryTellingRequest,
    story_teller: StoryTeller = Depends(get_story_teller),
    user = Depends(get_current_user)
):
    """
    Rewrites an experience to match a funding's requirements using LLM.
    """
    try:
        logger.info(f"Telling story for funding: {request.target_funding.name} (User: {user.email})")
        return story_teller.tell_story(
            request.experience, 
            request.target_funding
        )
    except Exception as e:
        error = format_error_response(e)
        logger.error(error)
        raise HTTPException(status_code=500, detail=error)

