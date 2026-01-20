from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from supabase import Client

from src.dependencies import get_current_user, supabase, get_ranker
from src.models import (
    FundingDefinition, FundingAgency, Experience, ExperienceType
)
from src.ranker import ExperienceRanker

router = APIRouter()

# Static Funding Definitions
FRQS_FUNDING = FundingDefinition(
    id="FRQS",
    name="Doctoral Training",
    agency=FundingAgency.FRQS,
    cycle_year="2025-2026",
    deadline=date(2025, 12, 17),
    website_url="https://frq.gouv.qc.ca/en/program/doctoral-training-master-s-degree-holders-2025-2026/"
)

CIHR_FUNDING = FundingDefinition(
    id="CIHR",
    name="CGS Doctoral Awards",
    agency=FundingAgency.CIHR,
    cycle_year="2025-2026",
    deadline=date(2025, 12, 17),
    website_url="https://cihr-irsc.gc.ca/e/193.html"
)

FUNDING_SOURCES = {
    "FRQS": FRQS_FUNDING,
    "CIHR": CIHR_FUNDING
}

class RankedExperienceResponse(BaseModel):
    experience: Experience
    score: int
    rationale: str

@router.get("/sources", response_model=List[FundingDefinition])
async def list_funding_sources(current_user = Depends(get_current_user)):
    """List available funding sources (FRQS, CIHR)"""
    return list(FUNDING_SOURCES.values())

@router.get("/{source_id}/experiences", response_model=List[RankedExperienceResponse])
async def get_ranked_experiences(
    source_id: str,
    current_user = Depends(get_current_user),
    ranker: ExperienceRanker = Depends(get_ranker)
):
    """
    Get all user experiences ranked against the specific funding source.
    """
    funding = FUNDING_SOURCES.get(source_id)
    if not funding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Funding source '{source_id}' not found"
        )
    
    # Fetch experiences from Supabase directly
    try:
        response = supabase.table("experiences") \
            .select("*") \
            .eq("user_id", current_user.id) \
            .execute()
        
        # Pydantic validation handles parsing
        experiences = [Experience(**item) for item in response.data]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch experiences: {str(e)}"
        )
        
    ranked_results = []
    
    # Rank each experience
    # TODO: In production, parallelize this or use a batch API
    for exp in experiences:
        try:
            rank_result = ranker.rank_experience(exp, funding)
            ranked_results.append(RankedExperienceResponse(
                experience=exp,
                score=rank_result.get("score", 0),
                rationale=rank_result.get("rationale", "No rationale generated.")
            ))
        except Exception as e:
            # If ranking fails for one, we allow it but log (or continue with 0 score)
            # For now, we just append with error note to not break the whole list
            print(f"Ranking failed for experience {exp.id}: {e}")
            ranked_results.append(RankedExperienceResponse(
                experience=exp,
                score=0,
                rationale="Ranking failed due to internal error."
            ))
            
    # Sort by score desc
    ranked_results.sort(key=lambda x: x.score, reverse=True)
    
    return ranked_results
