from unittest.mock import MagicMock
from src.remixer import ExperienceRemixer
from src.models import Experience, ExperienceType, FundingDefinition, FundingAgency
from datetime import date

def test_remixer_flow():
    """Test the remixer calls the LLM correctly."""
    mock_llm = MagicMock()
    mock_llm.generate_structured_data.return_value = {
        "experience_rating": 9,
        "remixed_description": "Better description",
        "rationale": "Because it is better"
    }
    
    remixer = ExperienceRemixer(mock_llm)
    
    exp = Experience(
        id="123",
        type=ExperienceType.PROFESSIONAL,
        title="Dev",
        organization="Corp",
        start_date=date(2022, 1, 1),
        description="I wrote code."
    )
    
    funding = FundingDefinition(
        id="funding1",
        name="Tech Funding",
        agency=FundingAgency.NSERC,
        cycle_year="2025",
        deadline=date(2025, 12, 1),
        website_url="https://example.com"
    )
    
    result = remixer.remix_experience(exp, funding)
    
    assert result.remixed_description == "Better description"
    assert result.experience_id == "123"
    assert result.experience_rating == 9
    mock_llm.generate_structured_data.assert_called_once()
