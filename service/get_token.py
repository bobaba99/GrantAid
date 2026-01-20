import os
import sys
import asyncio
from dotenv import load_dotenv
from supabase import create_client, Client

# Add parent directory to path to allow importing from src if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_token():
    # Load env from .env file
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        # Try loading from src/.env if root .env missing
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", ".env")
    
    load_dotenv(env_path)

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url or not key:
        print("Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env")
        return

    supabase: Client = create_client(url, key)

    print("Please enter your login credentials to get an access token.")
    email = input("Email: ")
    password = input("Password: ")

    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.session:
            print("\nSuccessfully logged in!")
            print("-" * 20)
            print(f"ACCESS TOKEN:\n{response.session.access_token}")
            print("-" * 20)
            print("\nUse this token in your curl command:")
            print(f'curl -H "Authorization: Bearer {response.session.access_token}" http://localhost:8000/api/funding/sources')
        else:
            print("Login failed: Try checking your email for a magic link or confirmation.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    get_token()
