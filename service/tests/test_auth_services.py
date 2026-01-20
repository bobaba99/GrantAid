import os
import sys
import uuid
from dotenv import load_dotenv
from supabase import create_client, Client, ClientOptions

# Try to load env from src/.env
load_dotenv("src/.env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: Missing Supabase credentials in src/.env")
    sys.exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def print_result(name, success, message=""):
    icon = "✅" if success else "❌"
    print(f"{icon} {name}: {message}")

def test_auth_workflow():
    print(f"\n🧪 Starting Auth Workflow Test")
    print(f"Using Supabase URL: {SUPABASE_URL}")
    print("-" * 50)

    # 1. Sign Up Test User
    email = f"test_auth_{uuid.uuid4().hex[:8]}@example.com"
    password = "TestPassword123!"
    
    user_id = None
    session_token = None

    print(f"📧 Attempting Sign Up with: {email}")
    try:
        response = supabase.auth.sign_up({
            "email": email, 
            "password": password
        })
        
        if response.user:
            user_id = response.user.id
            print_result("Sign Up", True, f"User created (ID: {user_id})")
            
            # Check if email confirmation is required
            if response.user.identities and response.user.identities[0].identity_data.get("email_verified", False):
                print("   ℹ️  Email is auto-verified.")
            elif response.session:
                 print("   ℹ️  Session returned immediately (Auto-confirm likely enabled).")
                 session_token = response.session.access_token
            else:
                print("   ⚠️  User created but no session. Email confirmation likely required.")
                print("   ⚠️  Cannot proceed with Sign In test for this user without manual verification.")
                
        else:
            print_result("Sign Up", False, "No user returned.")
            return

    except Exception as e:
        print_result("Sign Up", False, f"Exception: {str(e)}")
        return

    # 2. Sign In (If possible)
    if not session_token:
        print(f"\n🔑 Attempting Sign In (This may fail if email is not verified)")
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if response.session:
                session_token = response.session.access_token
                print_result("Sign In", True, "Successfully logged in")
            else:
                print_result("Sign In", False, "Login failed (likely unverified email)")
        except Exception as e:
             print_result("Sign In", False, f"Login failed: {str(e)}")

    # 3. Verify Session / Get User
    if session_token:
        print(f"\n🕵️  Verifying Session Token")
        try:
            user_response = supabase.auth.get_user(session_token)
            if user_response.user and user_response.user.email == email:
                print_result("Get User", True, "Token is valid and matches user")
            else:
                print_result("Get User", False, "Token verification failed")
        except Exception as e:
            print_result("Get User", False, f"Exception: {str(e)}")

    else:
        print("\n⚠️  Skipping 'Get User' and 'Sign Out' tests because we have no session.")

    # 4. Sign Out
    if session_token:
        print(f"\n👋 Attempting Sign Out")
        try:
            supabase.auth.sign_out()
            print_result("Sign Out", True, "Client signed out (Note: JWT does not expire immediately on server unless revoked)")
        except Exception as e:
            print_result("Sign Out", False, f"Exception: {str(e)}")

    # 5. Cleanup (Delete User)
    # This requires SERVICE_ROLE_KEY. If we are utilizing ANON_KEY, this will fail.
    # We try anyway if we have the ID.
    if user_id:
        print(f"\n🧹 Attempting Cleanup (Delete User)")
        is_service_role = os.getenv("SUPABASE_SERVICE_ROLE_KEY") is not None
        
        if is_service_role:
            try:
                # To delete a user, we usually need the admin api
                # The python client exposes auth.admin if instantiated with service key
                response = supabase.auth.admin.delete_user(user_id)
                print_result("Delete User", True, "Test user deleted successfully")
            except Exception as e:
                print_result("Delete User", False, f"Failed to delete user: {str(e)}")
        else:
            print("   ⚠️  Skipping cleanup: No SUPABASE_SERVICE_ROLE_KEY found in env.")
            print(f"   ℹ️  You may need to manually delete {email} from your Supabase dashboard.")

    print("\n✅ Test Complete")

if __name__ == "__main__":
    test_auth_workflow()
