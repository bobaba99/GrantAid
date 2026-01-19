from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.models import ExperienceType, GrantAgency
from main import app, get_remixer

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "GrantAid Backend"}

def test_remix_endpoint():
    # Mock the remixer dependency
    mock_remixer = MagicMock()
    mock_remixer.remix_experience.return_value = {
        "original_experience_id": "123",
        "remixed_description": "Mocked Description",
        "rationale": "Mocked Rationale"
    }
    
    app.dependency_overrides[get_remixer] = lambda: mock_remixer
    
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
        "target_grant": {
            "id": "g1",
            "name": "Grant",
            "agency": "NSERC",
            "cycle_year": "2025",
            "deadline": "2025-01-01",
            "website_url": "http://example.com"
        },
        "focus_keywords": ["Innovation"]
    }
    
    response = client.post("/remix", json=payload)
    assert response.status_code == 200
    assert response.json()["remixed_description"] == "Mocked Description"
    
    # Cleanup
    app.dependency_overrides = {}
