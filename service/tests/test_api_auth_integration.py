import os
import sys
import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from supabase import create_client

# Add service root to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Load env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", ".env")
load_dotenv(env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

@pytest.fixture
def auth_token():
    """Authenticates with Supabase and returns a valid access token."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        pytest.skip("Missing Supabase credentials")
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Create a unique test user if not exists, or sign in
    # For simplicity/speed in this test script, we'll try to sign in with a known test user 
    # OR create a temporary one.
    
    email = "test_api_integration@example.com"
    password = "TestPassword123!"
    
    try:
        # Try sign up
        up_res = supabase.auth.sign_up({"email": email, "password": password})
    except Exception:
        pass # User might exist
        
    try:
        # Sign in
        in_res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if in_res.session:
            return in_res.session.access_token
    except Exception as e:
        pytest.fail(f"Failed to obtain auth token: {e}")
    
    pytest.fail("Could not log in to get token")

def test_public_endpoint():
    """Test that public endpoints are accessible without token."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_protected_endpoint_no_token():
    """Test that protected endpoints reject requests without token."""
    client = TestClient(app)
    response = client.get("/me")
    # FastAPI Depends returns 401 or 403 depending on configuration
    # Our dependency raises 401
    assert response.status_code == 401

def test_protected_endpoint_valid_token(auth_token):
    """Test that protected endpoints accept valid tokens."""
    client = TestClient(app)
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = client.get("/me", headers=headers)
    
    if response.status_code != 200:
        print(f"Failed Response: {response.text}")
        
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert data["email"] == "test_api_integration@example.com"

if __name__ == "__main__":
    # Allow running directly
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("Please install httpx: pip install httpx")
        exit(1)
        
    print("Running manual test setup...")
    t = TestClient(app)
    
    # 1. Public
    print("Testing Public Endpoint...")
    r = t.get("/")
    print(f"Status: {r.status_code}")
    
    # 2. No Token
    print("Testing No Token...")
    r = t.get("/me")
    print(f"Status: {r.status_code} (Expected 401)")
    
    # 3. With Token
    print("Obtaining Token...")
    # reuse token logic manually
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    email = "test_api_integration@example.com"
    password = "TestPassword123!"
    try:
        supabase.auth.sign_up({"email": email, "password": password})
    except: pass
    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
    
    if res.session:
        print("Token obtained.")
        r = t.get("/me", headers={"Authorization": f"Bearer {res.session.access_token}"})
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")
    else:
        print("Failed to get token.")
