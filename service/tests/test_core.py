from unittest.mock import MagicMock
from src.story_teller import StoryTeller
from src.models import Experience, ExperienceType, FundingDefinition, FundingAgency
from datetime import date

def test_story_teller_flow():
    """Test the story teller calls the LLM correctly."""
    mock_llm = MagicMock()
    mock_llm.generate_structured_data.return_value = {
        "experience_rating": 9,
        "story": "Better description",
        "rationale": "Because it is better"
    }
    
    story_teller = StoryTeller(mock_llm)
    
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
    
    result = story_teller.tell_story(exp, funding)
    
    assert result.story == "Better description"
    assert result.experience_id == "123"
    assert result.experience_rating == 9
    mock_llm.generate_structured_data.assert_called_once()
