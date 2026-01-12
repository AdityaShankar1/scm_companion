import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app

load_dotenv()
client = TestClient(app)

def test_unauthorized_redirect():
    """Test that visiting the dashboard without a cookie redirects to login"""
    # Changed 303 to 307 to match FastAPI default
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/login"

def test_login_page_loads():
    response = client.get("/login")
    assert response.status_code == 200
    assert "Login" in response.text

def test_incorrect_login():
    response = client.post("/login", data={"username": "wrong", "password": "wrong"})
    assert "scm_session" not in response.cookies