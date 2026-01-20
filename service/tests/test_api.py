from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.models import ExperienceType, FundingAgency
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
        "experience_id": "123",
        "experience_rating": 8,
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
        "target_funding": {
            "id": "f1",
            "name": "Funding",
            "agency": "NSERC",
            "cycle_year": "2025",
            "deadline": "2025-01-01",
            "website_url": "http://example.com"
        }
    }
    
    response = client.post("/remix", json=payload)
    assert response.status_code == 200
    assert response.json()["remixed_description"] == "Mocked Description"
    assert response.json()["experience_rating"] == 8
    
    # Cleanup
    app.dependency_overrides = {}
