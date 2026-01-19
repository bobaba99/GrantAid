from unittest.mock import MagicMock
from src.remixer import ExperienceRemixer
from src.diff_engine import DiffEngine
from src.models import Experience, ExperienceType, GrantDefinition, GrantAgency, GrantRequirement
from datetime import date

def test_remixer_flow():
    """Test the remixer calls the LLM correctly."""
    mock_llm = MagicMock()
    mock_llm.generate_structured_data.return_value = {
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
    
    grant = GrantDefinition(
        id="grant1",
        name="Tech Grant",
        agency=GrantAgency.NSERC,
        cycle_year="2025",
        deadline=date(2025, 12, 1),
        website_url="https://example.com"
    )
    
    result = remixer.remix_experience(exp, grant)
    
    assert result.remixed_description == "Better description"
    assert result.original_experience_id == "123"
    mock_llm.generate_structured_data.assert_called_once()

def test_diff_engine_changes():
    """Test detecting changes in requirements."""
    engine = DiffEngine()
    
    req1 = GrantRequirement(id="1", category="CV", description="CV", max_words=500)
    req2 = GrantRequirement(id="2", category="CV", description="CV", max_words=1000) # Changed
    req3 = GrantRequirement(id="3", category="Statement", description="Statement") # New
    
    # Test Modification
    changes = engine.compare_requirements([req1], [req2])
    assert len(changes) == 1
    assert changes[0]["type"] == "MODIFIED"
    assert changes[0]["old_value"] == 500
    assert changes[0]["new_value"] == 1000
    
    # Test Addition
    changes = engine.compare_requirements([req1], [req1, req3])
    # Note: Logic compares by category. req1 matches req1. req3 is new.
    # changes should contain the addition of 'Statement'
    assert len(changes) == 1
    assert changes[0]["type"] == "ADDED"
    assert changes[0]["category"] == "Statement"
