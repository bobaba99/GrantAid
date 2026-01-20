from typing import List, Optional
from uuid import UUID
from src.dependencies import supabase
from src.models import Experience

class ExperienceService:
    async def list_experiences(self, user_id: str, skip: int = 0, limit: int = 50, category: Optional[str] = None) -> List[Experience]:
        query = supabase.table("experience").select("*").eq("user_id", user_id)
        if category:
            query = query.eq("type", category)
        
        # Supabase Python client pagination might differ, but select supports range or similar.
        # Actually basic .select() returns all, we can slice in mem or use range if supported.
        # For simplicity pending Supabase limit behavior, we just fetch.
        response = query.execute()
        
        # Sort client side or ensure DB sort? Default created_at usually.
        data = response.data
        return [Experience(**item) for item in data]

    async def create_experience(self, user_id: str, experience: Experience) -> Experience:
        # Pydantic model to dict, exclude None to let DB defaults work? 
        # But Experience model has ID optional.
        data = experience.dict(exclude={"id"}, exclude_none=True)
        data["user_id"] = user_id
        
        response = supabase.table("experience").insert(data).execute()
        if not response.data:
            raise Exception("Failed to create experience")
        return Experience(**response.data[0])

    async def get_experience(self, experience_id: str, user_id: str) -> Optional[Experience]:
        response = supabase.table("experience").select("*").eq("id", experience_id).eq("user_id", user_id).execute()
        if not response.data:
            return None
        return Experience(**response.data[0])

    async def update_experience(self, experience_id: str, user_id: str, experience_data: dict) -> Optional[Experience]:
        response = supabase.table("experience").update(experience_data).eq("id", experience_id).eq("user_id", user_id).execute()
        if not response.data:
             return None
        return Experience(**response.data[0])

    async def delete_experience(self, experience_id: str, user_id: str):
        supabase.table("experience").delete().eq("id", experience_id).eq("user_id", user_id).execute()
