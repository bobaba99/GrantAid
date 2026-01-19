from unittest.mock import MagicMock
from src.ranker import ExperienceRanker
from src.models import Experience, ExperienceType, GrantDefinition, GrantAgency
from datetime import date

def test_ranker_flow():
    """Test the ranker calls the LLM correctly."""
    mock_llm = MagicMock()
    mock_llm.generate_structured_data.return_value = {
        "score": 8,
        "rationale": "Relevant"
    }
    
    ranker = ExperienceRanker(mock_llm)
    
    exp = Experience(
        id="123",
        type=ExperienceType.PROFESSIONAL,
        title="Dev",
        organization="Corp",
        start_date=date(2022, 1, 1),
        description="Code"
    )
    grant = GrantDefinition(
        id="g1",
        name="Grant",
        agency=GrantAgency.NSERC,
        cycle_year="2025",
        deadline=date(2025, 12, 1),
        website_url="https://example.com"
    )
    
    result = ranker.rank_experience(exp, grant)
    
    assert result["score"] == 8
    assert result["rationale"] == "Relevant"
    mock_llm.generate_structured_data.assert_called_once()
