from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
from datetime import date

class ExperienceType(str, Enum):
    """Enumeration of experience types."""
    PROFESSIONAL = "Professional"
    ACADEMIC = "Academic"
    VOLUNTEER = "Volunteer"
    RESEARCH = "Research"

class FundingAgency(str, Enum):
    """Enumeration of funding agencies."""
    CIHR = "CIHR"
    FRQS = "FRQS"
    NSERC = "NSERC"

class Experience(BaseModel):
    """
    Represents a user's experience (professional, academic, etc.).
    """
    id: Optional[str] = Field(None, description="Unique identifier for the experience")
    type: ExperienceType = Field(..., description="Type of experience")
    title: str = Field(..., description="Title of the role or position")
    organization: str = Field(..., description="Organization or institution name")
    start_date: date = Field(..., description="Start date of the experience")
    end_date: Optional[date] = Field(None, description="End date (None if current)")
    description: str = Field(..., description="Detailed description of the experience")
    key_skills: List[str] = Field(default_factory=list, description="List of skills acquired")

class FundingDefinition(BaseModel):
    """
    Static information about a funding.
    """
    id: str = Field(..., description="Unique ID of the funding")
    name: str = Field(..., description="Name of the funding")
    agency: FundingAgency = Field(..., description="Funding agency")
    cycle_year: str = Field(..., description="Cycle year (e.g., 2025-2026)")
    deadline: date = Field(..., description="Application deadline")
    website_url: HttpUrl = Field(..., description="URL to the funding page")
    description: Optional[str] = Field(None, description="Detailed description/context of the funding")

class FundingVision(BaseModel):
    """
    Represents a funding agency's vision and mission.
    """
    agency: FundingAgency = Field(..., description="Funding agency")
    description: str = Field(..., description="Vision of the agency (includes objectives, values, mission, etc.)")

class StoryTellingRequest(BaseModel):
    """
    Request model for telling a story based on an experience.
    """
    experience: Experience = Field(..., description="The experience to use as a base")
    target_funding: FundingDefinition = Field(..., description="The target funding")

class StoryTellingResponse(BaseModel):
    """
    Response model for a told story.
    """
    experience_id: Optional[str] = Field(None, description="ID of the original experience")
    experience_rating: int = Field(..., description="Rating of the experience (1-10) to the funding agency's vision and requirements")
    story: str = Field(..., description="Rewritten description tailored to the funding agency's vision and requirements")
    rationale: str = Field(..., description="Rationale for the rating")

class ExperienceAnalysis(BaseModel):
    """
    Composite model containing the original experience and its analysis.
    """
    experience: Experience = Field(..., description="The original experience")
    analysis: StoryTellingResponse = Field(..., description="The storytelling analysis")
