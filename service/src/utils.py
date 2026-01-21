import logging
import json
from typing import Any, Dict
from datetime import date, datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("grantaid-service")

class DateTimeEncoder(json.JSONEncoder):
    """JSON Encoder for handling date and datetime objects."""
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.
    
    Args:
        name: The name of the logger (usually __name__).
        
    Returns:
        logging.Logger: The configured logger.
    """
    return logging.getLogger(name)

def sanitize_json_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitizes a dictionary to ensure it's JSON serializable (handling dates).
    
    Args:
        data: The dictionary to sanitize.
        
    Returns:
        Dict[str, Any]: The sanitized dictionary.
    """
    return json.loads(json.dumps(data, cls=DateTimeEncoder))

def format_error_response(error: Exception) -> Dict[str, str]:
    """
    Formats an exception into a standard error response dictionary.
    
    Args:
        error: The exception that occurred.
        
    Returns:
        Dict[str, str]: A dictionary with 'error' and 'details' keys.
    """
    logger.error(f"Error occurred: {str(error)}", exc_info=True)
    return {
        "error": type(error).__name__,
        "details": str(error)
    }

def load_grant_context(funding) -> str:
    """
    Attempts to load specific evaluation criteria from markdown files.
    Prioritizes:
    1. Exact match: {Agency}_{Name}_eval.md
    2. Agency fallback: {Agency}_eval.md
    """
    import os
    from pathlib import Path
    
    # Customize logger usage if needed, or pass it in
    logger = get_logger(__name__)
    
    # Normalize names for matching
    # funding is expected to be a FundingDefinition model
    agency = funding.agency.value
    name = funding.name.replace(" ", "_").replace("/", "-")
    
    base_path = Path(__file__).parent / "grant_context"
    
    candidates = []
    if base_path.exists():
        for file in base_path.glob("*.md"):
            if agency in file.name and "eval" in file.name:
                # Simple heuristic: if funding name parts are in filename
                if any(part in file.name for part in name.split("_") if len(part) > 2):
                    candidates.append(file)
    
    context = ""
    if candidates:
        best_match = max(candidates, key=lambda f: len(set(name.split("_")) & set(f.name.split("_"))))
        try:
            context = best_match.read_text()
            logger.info(f"Loaded context from {best_match.name}")
        except Exception as e:
            logger.warning(f"Failed to read context file {best_match}: {e}")
            
    return context

def load_evaluation_rubric(funding) -> str:
    """
    Loads the universal evaluation rubric from "Synthesized Rubric.md".
    
    Args:
        funding: FundingDefinition model (parameter kept for API consistency)
    
    Returns:
        str: Content of the evaluation rubric, or empty string if file not found
    """
    from pathlib import Path
    
    logger = get_logger(__name__)
    
    base_path = Path(__file__).parent / "grant_context"
    rubric_file = base_path / "Synthesized Rubric.md"
    
    context = ""
    try:
        if rubric_file.exists():
            context = rubric_file.read_text()
            logger.info(f"Loaded evaluation rubric from {rubric_file.name}")
        else:
            logger.warning(f"Evaluation rubric file not found: {rubric_file}")
    except Exception as e:
        logger.error(f"Failed to read evaluation rubric file {rubric_file}: {e}")
            
    return context