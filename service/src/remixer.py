from typing import List
from src.models import Experience, FundingDefinition, RemixedExperienceResponse
from src.llm_client import LLMClient
from src.utils import get_logger, sanitize_json_response

logger = get_logger(__name__)

class ExperienceRemixer:
    """
    Logic for rewriting user experiences to match funding requirements using an LLM.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def remix_experience(self, experience: Experience, target_funding: FundingDefinition) -> RemixedExperienceResponse:
        """
        Rewrites an experience description to align with a specific funding's values.
        
        Args:
            experience: The user's original experience.
            target_funding: The funding to tailor the experience for.
            
        Returns:
            RemixedExperienceResponse: The rewritten description and rationale.
        """
        logger.info(f"Remixing experience {experience.id} for funding {target_funding.name}")
        
        prompt = self._build_remix_prompt(experience, target_funding)
        
        # Define the expected JSON schema for the LLM
        schema = {
            "type": "OBJECT",
            "properties": {
                "experience_rating": {"type": "NUMBER"},
                "remixed_description": {"type": "STRING"},
                "rationale": {"type": "STRING"}
            },
            "required": ["experience_rating", "remixed_description", "rationale"]
        }
        
        try:
            result = self.llm.generate_structured_data(prompt, schema)
            
            return RemixedExperienceResponse(
                experience_id=experience.id,
                experience_rating=result["experience_rating"],
                remixed_description=result["remixed_description"],
                rationale=result["rationale"]
            )
        except Exception as e:
            logger.error(f"Failed to remix experience: {e}")
            raise

    def _build_remix_prompt(self, experience: Experience, target_funding: FundingDefinition) -> str:
        """
        Constructs the prompt for the LLM.
        """
        
        return f"""
        You are an expert academic grant writer. Your task is to rewrite a user's professional/academic experience to better align with a specific funding's objectives.
        
        Target Funding: {target_funding.name} ({target_funding.agency})
        Grant Agency Values/Mission: (The LLM should infer this from the agency name known to it)
        
        Original Experience:
        - Title: {experience.title}
        - Organization: {experience.organization}
        - Description: {experience.description}
        - Skills: {", ".join(experience.key_skills)}
        
        Instructions:
        1. Rewrite the "Description" to be more impactful and relevant to the {target_funding.agency}'s priorities.
        2. Keep the facts accurate but change the tone/emphasis.
        3. Provide a brief rationale for your changes.
        4. Rate the experience on a scale of 1-10, where 1 is the least relevant and 10 is the most relevant.
        """
