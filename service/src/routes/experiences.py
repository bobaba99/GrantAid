from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Optional, List
from src.models import Experience
from src.services.experience import ExperienceService
from src.dependencies import get_current_user

router = APIRouter()

def get_experience_service():
    return ExperienceService()

@router.get("/experiences", response_model=List[Experience])
async def list_experiences(
    current_user = Depends(get_current_user),
    service: ExperienceService = Depends(get_experience_service)
):
    """Get all experiences for authenticated user"""
    return await service.list_experiences(user_id=current_user.id)

@router.post("/experiences", response_model=Experience, status_code=201)
async def create_experience(
    experience: Experience,
    current_user = Depends(get_current_user),
    service: ExperienceService = Depends(get_experience_service)
):
    """Create new experience entry"""
    return await service.create_experience(current_user.id, experience)

@router.delete("/experiences/{experience_id}", status_code=204)
async def delete_experience(
    experience_id: str,
    current_user = Depends(get_current_user),
    service: ExperienceService = Depends(get_experience_service)
):
    """Delete experience"""
    await service.delete_experience(experience_id, current_user.id)