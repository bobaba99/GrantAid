from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.models import ExperienceType, FundingAgency
from main import app, get_story_teller, get_current_user

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "GrantAid Backend", "version": "1.0.0"}

def test_story_tell_endpoint():
    # Mock the story teller dependency
    mock_story_teller = MagicMock()
    mock_story_teller.tell_story.return_value = {
        "experience_id": "123",
        "experience_rating": 8,
        "story": "Mocked Story",
        "rationale": "Mocked Rationale"
    }
    
    app.dependency_overrides[get_story_teller] = lambda: mock_story_teller
    
    # Mock the current user dependency
    mock_user = MagicMock()
    mock_user.email = "test@example.com"
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    payload = {
        "experience": {
            "id": "123",
            "type": "Professional",
            "title": "Dev",
            "organization": "Corp",
            "start_date": "2023-01-01",
            "description": "Coded things",
            "key_skills": ["Python"]
        },
        "target_funding": {
            "id": "f1",
            "name": "Funding",
            "agency": "NSERC",
            "cycle_year": "2025",
            "deadline": "2025-01-01",
            "website_url": "http://example.com"
        }
    }
    
    response = client.post("/story-tell", json=payload)
    assert response.status_code == 200
    assert response.json()["story"] == "Mocked Story"
    assert response.json()["experience_rating"] == 8
    
    # Cleanup
    app.dependency_overrides = {}
