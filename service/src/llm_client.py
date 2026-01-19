import os
from google import genai
from google.genai import types
from src.utils import get_logger

logger = get_logger(__name__)

class LLMClient:
    """
    Client for interacting with Google's Gemini models via the GenAI SDK.
    """
    def __init__(self, api_key: str = None, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize the LLM client.
        
        Args:
            api_key: Google API key. Defaults to GOOGLE_API_KEY env var.
            model_name: The model to use.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not found. LLM features will fail.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

    def generate_text(self, prompt: str) -> str:
        """
        Generates text based on a prompt.
        
        Args:
            prompt: The input prompt.
            
        Returns:
            str: The generated text.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise

    def generate_structured_data(self, prompt: str, schema: dict) -> dict:
        """
        Generates structured data (JSON) based on a prompt and schema.
        
        Args:
            prompt: The input prompt.
            schema: The expected JSON schema.
            
        Returns:
            dict: The parsed JSON response.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema
                ),
            )
            return response.parsed
        except Exception as e:
            logger.error(f"Structured LLM generation failed: {e}")
            raise
