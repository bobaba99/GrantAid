from unittest.mock import MagicMock
from src.ranker import ExperienceRanker
from src.models import Experience, ExperienceType, FundingDefinition, FundingAgency
from datetime import date
import os

def test_ranker_context_loading():
    """Test that ranker loads context from markdown files."""
    mock_llm = MagicMock()
    mock_llm.generate_structured_data.return_value = {
        "score": 9,
        "rationale": "Perfect fit"
    }
    
    ranker = ExperienceRanker(mock_llm)
    
    exp = Experience(
        id="123",
        type=ExperienceType.ACADEMIC,
        title="Student",
        organization="Uni",
        start_date=date(2022, 1, 1),
        description="Studied hard."
    )
    
    # This name should match 'CIHR_CGRS-D_eval.md'
    funding = FundingDefinition(
        id="f1",
        name="CGRS-D",
        agency=FundingAgency.CIHR,
        cycle_year="2025",
        deadline=date(2025, 12, 1),
        website_url="https://example.com"
    )
    
    ranker.rank_experience(exp, funding)
    
    # Check the prompt sent to LLM
    args, _ = mock_llm.generate_structured_data.call_args
    prompt = args[0]
    
    # Verify markers from the prompt construction
    assert "Agency Evaluation Context:" in prompt
    
    # Verify content from the actual file 
    # (CIHR_CGRS-D_eval.md contains "Research potential" and "Indicators of research potential")
    assert "Research potential" in prompt
    assert "Indicators of research potential" in prompt
