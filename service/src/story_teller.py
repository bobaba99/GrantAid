from src.models import Experience, FundingDefinition, StoryTellingResponse
from src.llm_client import LLMClient
from src.utils import get_logger, load_grant_context, load_evaluation_rubric

logger = get_logger(__name__)

class StoryTeller:
    """
    Logic for rewriting user experiences to match funding requirements using an LLM.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def tell_story(self, experience: Experience, target_funding: FundingDefinition) -> StoryTellingResponse:
        """
        Rewrites an experience description to align with a specific funding's values, and provides a rating.
        
        Args:
            experience: The user's original experience.
            target_funding: The funding to tailor the experience for.
            
        Returns:
            StoryTellingResponse: The rewritten description, rating, and rationale.
        """
        logger.info(f"Telling story for experience {experience.id} for funding {target_funding.name}")
        
        prompt = self._build_story_prompt(experience, target_funding)
        
        # Define the expected JSON schema for the LLM with facet-based scoring
        # Field names match the SQL database columns
        schema = {
            "type": "OBJECT",
            "properties": {
                "experience_rating_facet_a": {"type": "INTEGER"},
                "experience_rating_facet_b": {"type": "INTEGER"},
                "experience_rating_facet_c": {"type": "INTEGER"},
                "experience_rating_facet_d": {"type": "INTEGER"},
                "story": {"type": "STRING"},
                "rationale": {"type": "STRING"}
            },
            "required": ["experience_rating_facet_a", "experience_rating_facet_b", 
                        "experience_rating_facet_c", "experience_rating_facet_d", 
                        "story", "rationale"]
        }
        
        try:
            result = self.llm.generate_structured_data(prompt, schema)
            
            return StoryTellingResponse(
                experience_id=experience.id,
                experience_rating_facet_a=result["experience_rating_facet_a"],
                experience_rating_facet_b=result["experience_rating_facet_b"],
                experience_rating_facet_c=result["experience_rating_facet_c"],
                experience_rating_facet_d=result["experience_rating_facet_d"],
                story=result["story"],
                rationale=result["rationale"]
            )
        except Exception as e:
            logger.error(f"Failed to tell story: {e}")
            raise

    def _build_story_prompt(self, experience: Experience, funding: FundingDefinition) -> str:
        """
        Constructs the prompt for the LLM using the facet-based evaluation rubric.
        """
        evaluation_rubric = load_evaluation_rubric(funding)
        
        return f"""
You are an expert academic grant writer specializing in Canadian research funding (CIHR, NSERC, FRQS). Your task is to evaluate and rewrite a user's experience using a facet-oriented rubric aligned with DORA principles.

Target Funding: {funding.name} ({funding.agency.value})
Website: {funding.website_url}

Evaluation Framework:
{evaluation_rubric}

Original Experience:
- Title: {experience.title}
- Organization: {experience.organization}
- Type: {experience.type.value}
- Description: {experience.description}
- Key Skills: {", ".join(experience.key_skills)}

Instructions:

1. EVALUATE the original experience using the four-facet rubric (score each 1-5):
   
   a) Facet A - Competency & Capacity (1-5):
      - Scientific/Methodological Expertise
      - Leadership & Mentorship
      - Transferable Skills Integration
   
   b) Facet B - Fit with Program Priorities (1-5):
      - Strategic Alignment with {funding.agency.value} priorities
      - EDI & Indigenous Research Integration
      - Knowledge Mobilization Capacity
   
   c) Facet C - Impact & Value (1-5):
      - Reach & Influence of Contributions
      - Evidence of Impact (DORA-aligned, not just metrics)
   
   d) Facet D - Narrative Flow & Coherence (1-5):
      - Storytelling & Identity
      - Clarity & Accessibility
      - Persuasion & Feasibility

2. REWRITE the experience description to maximize alignment with the rubric:
   - Transform passive descriptions into evidence of competency
   - Highlight transferable skills and leadership
   - Frame the experience using {funding.agency.value}-specific keywords
   - Focus on impact and outcomes, not just tasks
   - Create a compelling narrative that demonstrates strategic fit
   - Follow the "before and after" examples in Section 4 of the rubric

3. PROVIDE rationale explaining:
   - Why you assigned each facet score to the original experience
   - What specific improvements you made in the rewrite
   - How the rewritten version better aligns with {funding.agency.value} priorities

4. OUTPUT in JSON format with these exact field names:
   {{
     "experience_rating_facet_a": <1-5 integer>,
     "experience_rating_facet_b": <1-5 integer>,
     "experience_rating_facet_c": <1-5 integer>,
     "experience_rating_facet_d": <1-5 integer>,
     "story": "<rewritten experience description>",
     "rationale": "<explanation of scores and improvements>"
   }}

Remember: Use evidence-based language. Avoid generic adjectives. Focus on quality over quantity of outputs.
"""
