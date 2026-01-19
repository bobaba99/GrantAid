from typing import List
from src.models import Experience, GrantDefinition, RemixedExperienceResponse
from src.llm_client import LLMClient
from src.utils import get_logger, sanitize_json_response

logger = get_logger(__name__)

class ExperienceRemixer:
    """
    Logic for rewriting user experiences to match grant requirements using an LLM.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def remix_experience(self, experience: Experience, target_grant: GrantDefinition, focus_keywords: List[str] = []) -> RemixedExperienceResponse:
        """
        Rewrites an experience description to align with a specific grant's values.
        
        Args:
            experience: The user's original experience.
            target_grant: The grant to tailor the experience for.
            focus_keywords: Optional list of keywords to emphasize.
            
        Returns:
            RemixedExperienceResponse: The rewritten description and rationale.
        """
        logger.info(f"Remixing experience {experience.id} for grant {target_grant.name}")
        
        prompt = self._build_remix_prompt(experience, target_grant, focus_keywords)
        
        # Define the expected JSON schema for the LLM
        schema = {
            "type": "OBJECT",
            "properties": {
                "remixed_description": {"type": "STRING"},
                "rationale": {"type": "STRING"}
            },
            "required": ["remixed_description", "rationale"]
        }
        
        try:
            result = self.llm.generate_structured_data(prompt, schema)
            
            return RemixedExperienceResponse(
                original_experience_id=experience.id,
                remixed_description=result["remixed_description"],
                rationale=result["rationale"]
            )
        except Exception as e:
            logger.error(f"Failed to remix experience: {e}")
            raise

    def _build_remix_prompt(self, experience: Experience, grant: GrantDefinition, keywords: List[str]) -> str:
        """
        Constructs the prompt for the LLM.
        """
        keywords_str = ", ".join(keywords) if keywords else "None"
        
        return f"""
        You are an expert academic grant writer. Your task is to rewrite a user's professional/academic experience to better align with a specific grant's objectives.
        
        Target Grant: {grant.name} ({grant.agency})
        Grant Agency Values/Mission: (The LLM should infer this from the agency name known to it)
        
        Original Experience:
        - Title: {experience.title}
        - Organization: {experience.organization}
        - Description: {experience.description}
        - Skills: {", ".join(experience.key_skills)}
        
        Focus Keywords to Emphasize: {keywords_str}
        
        Instructions:
        1. Rewrite the "Description" to be more impactful and relevant to the {grant.agency}'s priorities.
        2. Keep the facts accurate but change the tone/emphasis.
        3. Provide a brief rationale for your changes.
        """
