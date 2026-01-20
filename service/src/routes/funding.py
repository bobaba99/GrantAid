from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.dependencies import get_current_user, supabase
from src.models import (
    FundingDefinition, FundingAgency
)

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
