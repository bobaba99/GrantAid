from unittest.mock import MagicMock, patch
from src.llm_client import LLMClient

@patch("src.llm_client.genai.Client")
def test_llm_generate_text(mock_client_class):
    """Test clean text generation."""
    # Mock response
    mock_response = MagicMock()
    mock_response.text = "Generated content"
    
    # Mock client instance
    mock_instance = mock_client_class.return_value
    mock_instance.models.generate_content.return_value = mock_response

    client = LLMClient(api_key="fake_key")
    result = client.generate_text("Test prompt")
    
    assert result == "Generated content"
    mock_instance.models.generate_content.assert_called_once()
