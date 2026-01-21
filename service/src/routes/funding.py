from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.dependencies import get_current_user, supabase
from src.models import (
    FundingDefinition, FundingAgency, Experience, ExperienceAnalysis, ExperienceAnalysisResponse
)
from src.story_teller import StoryTeller
from src.dependencies import get_story_teller

router = APIRouter()

@router.get("/fundings", response_model=List[FundingDefinition])
async def get_all_fundings(current_user = Depends(get_current_user)):
    """List available funding sources"""
    try:
        response = supabase.table("funding").select("*").execute()
        return [FundingDefinition(**item) for item in response.data]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch fundings: {str(e)}"
        )

@router.get("/fundings/{funding_id}", response_model=FundingDefinition)
async def get_funding(funding_id: str, current_user = Depends(get_current_user)):
    """Get a specific funding source by ID"""
    try:
        # We assume the ID passed is the UUID or we query by 'id' column
        # Ideally the frontend sends the UUID. If 'funding_id' in frontend is 'FRQS', 
        # we might need to change frontend to use UUIDs or query by name/agency.
        # But wait, looking at the seed, the IDs are generated UUIDs in DB? 
        # No, wait, previous code used "FRQS" as ID. 
        # The seed file uses "INSERT INTO public.funding (name...)" and ID is generated.
        # So frontend needs to use the UUIDs returned by get_all_fundings.
        
        response = supabase.table("funding").select("*").eq("id", funding_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Funding not found")
            
        return FundingDefinition(**response.data[0])
    except Exception as e:
         # If UUID is invalid, supabase might throw.
        raise HTTPException(status_code=404, detail=f"Funding not found or error: {str(e)}")

@router.get("/fundings/{funding_id}/analyses", response_model=List[ExperienceAnalysisResponse])
async def get_funding_analyses(
    funding_id: str,
    current_user = Depends(get_current_user)
):
    """Get existing analyses for a funding without re-generating"""
    try:
        # Fetch analyses
        analyses_response = supabase.table("experience_analysis")\
            .select("*")\
            .eq("user_id", current_user.id)\
            .eq("funding_id", funding_id)\
            .execute()
        
        if not analyses_response.data:
            return []

        analyses_data = analyses_response.data
        experience_ids = [a['experience_id'] for a in analyses_data]
        
        # Fetch related experiences
        experiences_response = supabase.table("experience")\
            .select("*")\
            .in_("id", experience_ids)\
            .execute()
            
        experiences_map = {e['id']: Experience(**e) for e in experiences_response.data}
        
        results = []
        from src.models import StoryTellingResponse
        
        for item in analyses_data:
            exp_id = item['experience_id']
            if exp_id in experiences_map:
                analysis = StoryTellingResponse(
                    experience_id=exp_id,
                    experience_rating_facet_a=item['experience_rating_facet_a'],
                    experience_rating_facet_b=item['experience_rating_facet_b'],
                    experience_rating_facet_c=item['experience_rating_facet_c'],
                    experience_rating_facet_d=item['experience_rating_facet_d'],
                    story=item['story'],
                    rationale=item['rationale']
                )
                results.append(ExperienceAnalysisResponse(
                    experience=experiences_map[exp_id],
                    analysis=analysis
                ))
                
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch analyses: {str(e)}")



@router.post("/fundings/{funding_id}/analyze-experiences", response_model=List[ExperienceAnalysisResponse])
def analyze_experiences(
    funding_id: str,
    force_refresh: bool = False,
    story_teller: StoryTeller = Depends(get_story_teller),
    current_user = Depends(get_current_user)
):
    """
    Analyzes all user experiences against the specified funding criteria.
    """
    try:
        # 1. Fetch Funding
        funding_response = supabase.table("funding").select("*").eq("id", funding_id).execute()
        if not funding_response.data:
            raise HTTPException(status_code=404, detail="Funding not found")
        funding = FundingDefinition(**funding_response.data[0])

        # 2. Fetch User Experiences
        exp_response = supabase.table("experience").select("*").eq("user_id", current_user.id).execute()
        experiences_data = exp_response.data
        
        # 3. Fetch Existing Analyses
        # Fetch all analyses for this user and funding to batch check
        existing_analyses_response = supabase.table("experience_analysis")\
            .select("*")\
            .eq("user_id", current_user.id)\
            .eq("funding_id", funding_id)\
            .execute()
            
        existing_analyses_map = {item['experience_id']: item for item in existing_analyses_response.data}
        
        results = []
        import json
        from src.models import StoryTellingResponse

        for exp_data in experiences_data:
            # Pydantic validation
            experience = Experience(**exp_data)
            
            # Check cache
            if experience.id in existing_analyses_map and not force_refresh:
                cached_data = existing_analyses_map[experience.id]
                analysis = StoryTellingResponse(
                    experience_id=cached_data['experience_id'],
                    experience_rating_facet_a=cached_data['experience_rating_facet_a'],
                    experience_rating_facet_b=cached_data['experience_rating_facet_b'],
                    experience_rating_facet_c=cached_data['experience_rating_facet_c'],
                    experience_rating_facet_d=cached_data['experience_rating_facet_d'],
                    story=cached_data['story'],
                    rationale=cached_data['rationale']
                )
            else:
                # Generate new
                analysis = story_teller.tell_story(experience, funding)
                
                # Save to DB
                try:
                    insert_data = {
                        "user_id": current_user.id,
                        "experience_id": experience.id,
                        "funding_id": funding.id,
                        "story": analysis.story,
                        "rationale": analysis.rationale,
                        "experience_rating_facet_a": analysis.experience_rating_facet_a,
                        "experience_rating_facet_b": analysis.experience_rating_facet_b,
                        "experience_rating_facet_c": analysis.experience_rating_facet_c,
                        "experience_rating_facet_d": analysis.experience_rating_facet_d
                    }
                    supabase.table("experience_analysis").upsert(insert_data).execute()
                except Exception as save_err:
                    # Log but don't fail the request if saving fails?
                    # Or maybe fail? Let's log and continue to return the result to user at least.
                    print(f"Failed to save analysis for exp {experience.id}: {save_err}")

            results.append(ExperienceAnalysisResponse(
                experience=experience,
                analysis=analysis
            ))
            
        return results

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
