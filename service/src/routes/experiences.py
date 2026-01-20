# app/routers/experiences.py
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.schemas.experience import ExperienceCreate, ExperienceUpdate, ExperienceResponse
from app.services.experience_service import ExperienceService
from app.dependencies import get_current_user, get_experience_service

router = APIRouter()

@router.get("/", response_model=list[ExperienceResponse])
async def list_experiences(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    current_user = Depends(get_current_user),
    experience_service: ExperienceService = Depends(get_experience_service)
):
    """Get all experiences for authenticated user with optional filtering"""
    return await experience_service.list_experiences(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        category=category
    )

@router.post("/", response_model=ExperienceResponse, status_code=201)
async def create_experience(
    experience: ExperienceCreate,
    current_user = Depends(get_current_user),
    experience_service: ExperienceService = Depends(get_experience_service)
):
    """Create new experience entry"""
    return await experience_service.create_experience(current_user.id, experience)

@router.get("/{experience_id}", response_model=ExperienceResponse)
async def get_experience(
    experience_id: str,
    current_user = Depends(get_current_user),
    experience_service: ExperienceService = Depends(get_experience_service)
):
    """Get specific experience by ID"""
    return await experience_service.get_experience(experience_id, current_user.id)

@router.patch("/{experience_id}", response_model=ExperienceResponse)
async def update_experience(
    experience_id: str,
    experience_data: ExperienceUpdate,
    current_user = Depends(get_current_user),
    experience_service: ExperienceService = Depends(get_experience_service)
):
    """Update existing experience"""
    return await experience_service.update_experience(
        experience_id, current_user.id, experience_data
    )

@router.delete("/{experience_id}", status_code=204)
async def delete_experience(
    experience_id: str,
    current_user = Depends(get_current_user),
    experience_service: ExperienceService = Depends(get_experience_service)
):
    """Delete experience"""
    await experience_service.delete_experience(experience_id, current_user.id)