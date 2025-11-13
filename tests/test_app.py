import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    # Check participant is added
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]


def test_unregister_participant():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure participant exists
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    # Check participant is removed
    get_resp = client.get("/activities")
    assert email not in get_resp.json()[activity]["participants"]
