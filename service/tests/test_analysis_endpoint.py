from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.models import Experience, FundingDefinition, StoryTellingResponse, ExperienceAnalysis
from main import app, get_story_teller, get_current_user
from src.dependencies import supabase

client = TestClient(app)

def test_analyze_experiences_endpoint():
    # 1. Mock StoryTeller
    mock_story_teller = MagicMock()
    mock_story_teller.tell_story.return_value = StoryTellingResponse(
        experience_id="exp1",
        experience_rating=9,
        story="Cool story",
        rationale="Matches perfectly"
    )
    app.dependency_overrides[get_story_teller] = lambda: mock_story_teller
    
    # 2. Mock Current User
    mock_user = MagicMock()
    mock_user.id = "user1"
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    # 3. Mock Supabase (tricky part)
    # We need to mock the supabase client imported in funding.py
    # Since we can't easily patch the global 'supabase' variable in funding.py from here 
    # without patching 'src.routes.funding.supabase', let's try pushing a mock.
    
    from src.routes import funding
    original_supabase = funding.supabase
    
    mock_supabase = MagicMock()
    # Mock funding fetch
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{
        "id": "fund1",
        "name": "Funding 1",
        "agency": "NSERC",
        "cycle_year": "2025",
        "deadline": "2025-01-01",
        "website_url": "http://example.com"
    }]
    
    # When fetching experiences, return one experience
    # The chain is table -> select -> eq -> execute
    # Ideally logic distinguishes calls. 
    # Mocking side_effect based on table name is better.
    
    def side_effect_table(name):
        mock_query = MagicMock()
        if name == "funding":
            mock_query.select.return_value.eq.return_value.execute.return_value.data = [{
                "id": "fund1",
                "name": "Funding 1",
                "agency": "NSERC",
                "cycle_year": "2025",
                "deadline": "2025-01-01",
                "website_url": "http://example.com"
            }]
        elif name == "experience":
            mock_query.select.return_value.eq.return_value.execute.return_value.data = [{
                "id": "exp1",
                "type": "Professional",
                "title": "Software Engineer",
                "organization": "Google",
                "start_date": "2020-01-01",
                "description": "Wrote code",
                "key_skills": ["Python"]
            }]
        elif name == "experience_analysis":
             # Simulate no existing analysis initially
             mock_query.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = []
        return mock_query

    mock_supabase.table.side_effect = side_effect_table
    funding.supabase = mock_supabase
    
    try:
        response = client.post("/api/funding/fundings/fund1/analyze-experiences")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["experience"]["title"] == "Software Engineer"
        assert data[0]["analysis"]["experience_rating"] == 9
        assert data[0]["analysis"]["story"] == "Cool story"
        
    finally:
        # Restore
        funding.supabase = original_supabase
        app.dependency_overrides = {}
