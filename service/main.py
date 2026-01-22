import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.models import (
    Experience, FundingDefinition, StoryTellingRequest, 
    StoryTellingResponse, UserProfile
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
    allow_origins=["http://localhost:5173", "https://grantaid.onrender.com", "https://grantaid-backend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(funding.router, prefix="/api/funding", tags=["funding"])
from src.routes import experiences
app.include_router(experiences.router, prefix="/api", tags=["experiences"])

@app.get("/")
@app.head("/")
def read_root():
    return {"status": "ok", "service": "GrantAid Backend", "version": "1.0.0"}

@app.get("/me")
def read_current_user(user = Depends(get_current_user)):
    try:
        # Check 'profiles' table for additional info
        profile_response = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
        profile_data = profile_response.data if profile_response.data else {}
    except Exception as e:
        # If profile doesn't exist (PGRST116), create it
        if "PGRST116" in str(e) or getattr(e, "code", "") == "PGRST116":
             logger.info(f"Profile not found for {user.id}, creating default profile.")
             try:
                 new_profile = {"id": user.id}
                 # Insert default profile
                 insert_res = supabase.table("profiles").insert(new_profile).execute()
                 profile_data = insert_res.data[0] if insert_res.data else {}
             except Exception as create_error:
                 logger.error(f"Failed to create default profile for {user.id}: {create_error}")
                 profile_data = {}
        else:
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

@app.put("/me")
def update_current_user(
    profile: UserProfile,
    user = Depends(get_current_user)
):
    """
    Update the authenticated user's profile information.
    """
    try:
        profile_data = profile.dict(exclude_none=True)
        profile_data["id"] = user.id
        # Also store email if not present in profiles table? 
        # Usually profiles table is linked by id. Let's just upsert the fields.
        
        # Upsert into profiles table
        response = supabase.table("profiles").upsert(profile_data).execute()
        
        if not response.data:
            # If nothing returned, it might check if success anyway
            pass

        return {
            "status": "success",
            "message": "Profile updated successfully",
            "data": profile_data
        }
    except Exception as e:
        logger.error(f"Failed to update profile for {user.id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")


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

