from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to ChatGPT-like API"}

def test_query():
    response = client.post("/query", json={"query": "Hello, ChatGPT"})
    assert response.status_code == 200
    assert response.json() == {"response": "Simulated response for: Hello, ChatGPT"}
