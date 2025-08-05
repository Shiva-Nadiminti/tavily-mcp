from pydantic import BaseModel, Field
from typing import Optional, List

class SearchRequest(BaseModel):
    """Request model for simple search"""
    query: str = Field(..., min_length=1, example="latest AI research")

class AdvancedSearchRequest(BaseModel):
    """Request model for advanced search"""
    query: str = Field(..., min_length=1, example="machine learning")
    max_results: Optional[int] = Field(5, gt=0, le=20, example=5)
    include_domains: Optional[List[str]] = Field(
        None, 
        example=["arxiv.org", "medium.com"]
    )
    exclude_domains: Optional[List[str]] = Field(
        None,
        example=["wikipedia.org"]
    )