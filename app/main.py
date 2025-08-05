from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Optional, List
from app.tavily_client import TavilyClient
from app.schemas import SearchRequest, AdvancedSearchRequest
from app.config import settings
import os

app = FastAPI(
    title="Tavily MCP Server",
    description="MCP server for Tavily AI search engine",
    version="0.1.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Serve static files (for favicon)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Tavily client
tavily = TavilyClient(api_key=settings.tavily_api_key)

@app.get("/", include_in_schema=False)
async def root():
    """Redirect root URL to /docs"""
    return RedirectResponse(url="/docs")

@app.get("/api-info")
async def api_info():
    """Endpoint that provides basic information about the API"""
    return JSONResponse(
        content={
            "message": "Tavily MCP Server is running",
            "documentation": "/docs",
            "endpoints": {
                "simple_search": {
                    "path": "/simple_search",
                    "method": "POST",
                    "description": "Perform a basic search"
                },
                "advanced_search": {
                    "path": "/advanced_search",
                    "method": "POST",
                    "description": "Perform search with filters"
                },
                "get_search_results": {
                    "path": "/get_search_results/{search_id}",
                    "method": "GET",
                    "description": "Retrieve previous search results"
                },
                "check_api_usage": {
                    "path": "/check_api_usage",
                    "method": "GET",
                    "description": "Check API usage statistics"
                }
            }
        }
    )

@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    """Endpoint for favicon requests"""
    favicon_path = "static/favicon.ico"
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    return JSONResponse(
        status_code=404,
        content={"message": "No favicon available"}
    )

@app.post("/simple_search")
async def simple_search(request: SearchRequest):
    """
    Perform a simple search using Tavily AI search engine.
    
    Parameters:
    - query: The search query string (required)
    
    Returns:
    - List of search results with title, url, and content
    - Search ID for reference
    """
    try:
        results = tavily.simple_search(request.query)
        return {
            "status": "success",
            "data": results,
            "search_id": results.get("id")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/advanced_search")
async def advanced_search(request: AdvancedSearchRequest):
    """
    Perform an advanced search with additional parameters.
    
    Parameters:
    - query: The search query string (required)
    - max_results: Maximum number of results to return (default: 5)
    - include_domains: List of domains to include in search
    - exclude_domains: List of domains to exclude from search
    
    Returns:
    - List of filtered search results
    - Search ID for reference
    """
    try:
        results = tavily.advanced_search(
            query=request.query,
            max_results=request.max_results,
            include_domains=request.include_domains,
            exclude_domains=request.exclude_domains
        )
        return {
            "status": "success",
            "data": results,
            "search_id": results.get("id")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_search_results/{search_id}")
async def get_search_results(search_id: str):
    """
    Retrieve results from a previous search by ID.
    
    Parameters:
    - search_id: The ID of a previous search
    
    Returns:
    - The original search results if found
    """
    try:
        results = tavily.get_search_results(search_id)
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Search not found")

@app.get("/check_api_usage")
async def check_api_usage():
    """
    Check current API usage statistics.
    
    Returns:
    - Current usage metrics
    - Rate limit information
    """
    try:
        usage = tavily.check_api_usage()
        return {"status": "success", "data": usage}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Validation failed",
            "details": exc.errors(),
            "suggestion": "Ensure your request matches the expected format"
        },
    )