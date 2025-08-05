import pytest
from app.tavily_client import TavilyClient

@pytest.fixture
def tavily_client():
    return TavilyClient()

def test_tavily_client_initialization(tavily_client):
    assert tavily_client is not None

def test_some_api_functionality(tavily_client):
    # Assuming there is a method called `some_api_method` in TavilyClient
    response = tavily_client.some_api_method()
    assert response is not None
    assert isinstance(response, dict)  # Adjust based on expected response type

def test_error_handling(tavily_client):
    # Assuming there is a method that raises an exception for invalid input
    with pytest.raises(ValueError):
        tavily_client.some_api_method(invalid_input=True)  # Adjust based on actual method signature