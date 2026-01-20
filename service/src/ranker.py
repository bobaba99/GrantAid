from typing import List
from src.models import Experience, FundingDefinition
from src.llm_client import LLMClient
from src.utils import get_logger, load_grant_context

logger = get_logger(__name__)

class ExperienceRanker:
    """
    Logic for ranking experiences against grant requirements.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def rank_experience(self, experience: Experience, target_funding: FundingDefinition) -> dict:
        """
        Generates a relevance score and rationale for an experience given a grant.
        
        Args:
            experience: The experience to evaluate.
            target_funding: The grant to evaluate against.
            
        Returns:
            dict: {"score": int, "rationale": str}
        """
        logger.info(f"Ranking experience {experience.id} for grant {target_funding.name}")
        
        prompt = self._build_ranking_prompt(experience, target_funding)
        
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

    def _build_ranking_prompt(self, experience: Experience, target_funding: FundingDefinition) -> str:
        context_text = load_grant_context(target_funding)
        
        return f"""
        You are an expert funding evaluator. Rate the relevance of the following experience for the specific funding opportunity.
        Evaluate experiences against the agency's evaluation criteria.
        
        Target Funding: {target_funding.name} ({target_funding.agency})
        
        Agency Evaluation Context:
        {context_text}
        
        Experience:
        - Title: {experience.title}
        - Organization: {experience.organization}
        - Description: {experience.description}
        - Skills: {", ".join(experience.key_skills)}
        
        Instructions:
        1. Score the relevance from 1 to 10 (10 being perfectly aligned).
        2. Provide a 1-sentence narrative of how this experience fits the agency's funding goals and visions.
        3. Provide a 1-sentence rationale for the score and integration.
        """

