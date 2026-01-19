from typing import List
from src.models import Experience, GrantDefinition
from src.llm_client import LLMClient
from src.utils import get_logger

logger = get_logger(__name__)

class ExperienceRanker:
    """
    Logic for ranking experiences against grant requirements.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def rank_experience(self, experience: Experience, target_grant: GrantDefinition) -> dict:
        """
        Generates a relevance score and rationale for an experience given a grant.
        
        Args:
            experience: The experience to evaluate.
            target_grant: The grant to evaluate against.
            
        Returns:
            dict: {"score": int, "rationale": str}
        """
        logger.info(f"Ranking experience {experience.id} for grant {target_grant.name}")
        
        prompt = self._build_ranking_prompt(experience, target_grant)
        
        schema = {
            "type": "OBJECT",
            "properties": {
                "score": {"type": "INTEGER"},
                "rationale": {"type": "STRING"}
            },
            "required": ["score", "rationale"]
        }
        
        try:
            return self.llm.generate_structured_data(prompt, schema)
        except Exception as e:
            logger.error(f"Failed to rank experience: {e}")
            raise

    def _build_ranking_prompt(self, experience: Experience, grant: GrantDefinition) -> str:
        return f"""
        You are an expert academic evaluator. Rate the relevance of the following experience for the specific grant.
        
        Target Grant: {grant.name} ({grant.agency})
        
        Experience:
        - Title: {experience.title}
        - Organization: {experience.organization}
        - Description: {experience.description}
        - Skills: {", ".join(experience.key_skills)}
        
        Instructions:
        1. Score the relevance from 1 to 10 (10 being perfectly aligned).
        2. Provide a 1-sentence rationale for the score.
        """
