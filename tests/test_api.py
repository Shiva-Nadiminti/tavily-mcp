from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Tavily MCP!"}

def test_some_endpoint():
    response = client.get("/some-endpoint")
    assert response.status_code == 200
    assert "data" in response.json()  # Adjust based on actual response structure

def test_post_endpoint():
    response = client.post("/post-endpoint", json={"key": "value"})
    assert response.status_code == 201
    assert response.json() == {"success": True}  # Adjust based on actual response structure