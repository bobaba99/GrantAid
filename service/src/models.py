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

class GrantAgency(str, Enum):
    """Enumeration of grant agencies."""
    CIHR = "CIHR"
    NSERC = "NSERC"
    SSHRC = "SSHRC"
    FRQNT = "FRQNT"
    FRQSC = "FRQSC"
    FRQS = "FRQS"
    OTHER = "Other"

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

class GrantRequirement(BaseModel):
    """
    Represents a specific requirement for a grant application.
    """
    id: str = Field(..., description="Unique ID of the requirement")
    category: str = Field(..., description="Category (e.g., CV, Personal Statement)")
    description: str = Field(..., description="Description of the requirement")
    max_words: Optional[int] = Field(None, description="Maximum word count")
    format_rules: Optional[dict] = Field(None, description="Formatting rules (margins, font, etc.)")

class GrantDefinition(BaseModel):
    """
    Static information about a grant.
    """
    id: str = Field(..., description="Unique ID of the grant")
    name: str = Field(..., description="Name of the grant")
    agency: GrantAgency = Field(..., description="Funding agency")
    cycle_year: str = Field(..., description="Cycle year (e.g., 2025-2026)")
    deadline: date = Field(..., description="Application deadline")
    website_url: HttpUrl = Field(..., description="URL to the grant page")
    requirements: List[GrantRequirement] = Field(default_factory=list, description="List of requirements")

class RemixedExperienceRequest(BaseModel):
    """
    Request model for remixing an experience.
    """
    experience: Experience = Field(..., description="The experience to remix")
    target_grant: GrantDefinition = Field(..., description="The target grant definition")
    focus_keywords: List[str] = Field(default_factory=list, description="Keywords to emphasize")

class RemixedExperienceResponse(BaseModel):
    """
    Response model for a remixed experience.
    """
    original_experience_id: Optional[str] = Field(None, description="ID of the original experience")
    remixed_description: str = Field(..., description="Rewritten description tailored to the grant")
    rationale: str = Field(..., description="Explanation of changes made")
