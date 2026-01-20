import requests
from bs4 import BeautifulSoup
from src.utils import get_logger, format_error_response

logger = get_logger(__name__)

class GrantScraper:
    """
    Logic for fetching and parsing grant agency websites.
    """
    
    def fetch_grant_page(self, url: str) -> str:
        """
        Fetches the HTML content of a grant page.
        
        Args:
            url: The URL to fetch.
            
        Returns:
            str: The HTML content.
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise

    def parse_grant_details(self, html_content: str) -> dict:
        """
        Parses HTML content to extract grant details.
        Note: This is a heuristic-based parser and would need to be tailored for specific agencies.
        
        Args:
            html_content: Raw HTML.
            
        Returns:
            dict: Extracted details (title, deadline, description).
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Heuristic extraction (placeholders for agency-specific logic)
        title = soup.title.string if soup.title else "Unknown Title"
        
        # Clean text
        text_content = soup.get_text(separator="\n", strip=True)
        
        return {
            "title": title.strip(),
            "raw_text_summary": text_content[:500] + "..." # truncated
        }
