from unittest.mock import MagicMock, patch
from src.scraper import GrantScraper

@patch("src.scraper.requests.get")
def test_fetch_grant_page(mock_get):
    """Test fetching a page."""
    mock_response = MagicMock()
    mock_response.text = "<html><body><h1>Grant</h1></body></html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    scraper = GrantScraper()
    content = scraper.fetch_grant_page("http://example.com")
    
    assert content == "<html><body><h1>Grant</h1></body></html>"
    mock_get.assert_called_once()

def test_parse_grant_details():
    """Test parsing logic."""
    html = "<html><head><title>Test Grant</title></head><body><p>Deadline: 2025</p></body></html>"
    scraper = GrantScraper()
    details = scraper.parse_grant_details(html)
    
    assert details["title"] == "Test Grant"
    assert "Deadline: 2025" in details["raw_text_summary"]
