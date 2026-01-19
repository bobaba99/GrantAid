import os
from supabase import create_client, Client
from src.utils import get_logger

logger = get_logger(__name__)

class SupabaseService:
    """
    Service for interacting with Supabase.
    """
    _instance: Client = None

    @classmethod
    def get_client(cls) -> Client:
        """
        Returns the singleton Supabase client.
        """
        if cls._instance is None:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            
            if not url or not key:
                logger.warning("SUPABASE_URL or SUPABASE_KEY not set. DB operations will fail.")
            
            try:
                cls._instance = create_client(url, key)
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                raise

        return cls._instance
