import unittest
from fastapi.testclient import TestClient
from app.core.main import app

client = TestClient(app)

class TestMain(unittest.TestCase):

    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to ChatGPT-like API"}

    def test_query(self):
        response = client.post("/query", json={"query": "¿quien es zara?"})
        assert response.status_code == 200
        assert response.json() == {"response": "Zara 🚀 es un explorador intrépido y valiente 🏃♂️🏹, que viaja en busca de la paz para su galaxy 🌌, en la lejana galaxia de"}

if __name__ == "__main__":
    unittest.main()