import pytest
from datetime import date
from src.models import Experience, ExperienceType
from src.utils import sanitize_json_response

def test_experience_model_valid():
    """Test creating a valid Experience model."""
    exp = Experience(
        type=ExperienceType.PROFESSIONAL,
        title="Software Engineer",
        organization="Tech Corp",
        start_date=date(2020, 1, 1),
        description="Worked on backend systems."
    )
    assert exp.title == "Software Engineer"
    assert exp.type == ExperienceType.PROFESSIONAL

def test_experience_model_invalid_type():
    """Test validation error for invalid experience type."""
    with pytest.raises(ValueError):
        Experience(
            type="InvalidType",
            title="Software Engineer",
            organization="Tech Corp",
            start_date=date(2020, 1, 1),
            description="Worked on backend systems."
        )

def test_sanitize_json_response():
    """Test JSON sanitization handles date objects."""
    data = {"date": date(2023, 1, 1), "name": "Test"}
    sanitized = sanitize_json_response(data)
    assert sanitized["date"] == "2023-01-01"
    assert sanitized["name"] == "Test"
