import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_auth_access_token():
    response = client.post("/api/v1/auth/login/access-token", data={"username": "fake", "password": "fake"})
    assert response.status_code in (400, 422) 