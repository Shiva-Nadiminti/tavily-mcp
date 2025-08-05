import requests
from typing import Optional, List
from pydantic import BaseModel

class TavilyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tavily.com"
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        })

    def simple_search(self, query: str) -> dict:
        """Perform a simple search"""
        payload = {
            "query": query,
            "search_depth": "basic"
        }
        response = self.session.post(f"{self.base_url}/search", json=payload)
        response.raise_for_status()
        return response.json()

    def advanced_search(self, query: str, max_results: int = 5,
                       include_domains: Optional[List[str]] = None,
                       exclude_domains: Optional[List[str]] = None) -> dict:
        """Perform an advanced search with filters"""
        payload = {
            "query": query,
            "max_results": max_results,
            "search_depth": "advanced",
            "include_domains": include_domains or [],
            "exclude_domains": exclude_domains or []
        }
        response = self.session.post(f"{self.base_url}/search", json=payload)
        response.raise_for_status()
        return response.json()

    def get_search_results(self, search_id: str) -> dict:
        """Retrieve previous search results"""
        response = self.session.get(f"{self.base_url}/searches/{search_id}")
        response.raise_for_status()
        return response.json()

    def check_api_usage(self) -> dict:
        """Check API usage statistics"""
        response = self.session.get(f"{self.base_url}/usage")
        response.raise_for_status()
        return response.json()