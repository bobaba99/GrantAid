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
