"""Shared fixtures for tests."""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def test_activities():
    """Provide a fresh copy of test activities data for each test."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }


@pytest.fixture
def client(test_activities, monkeypatch):
    """Provide a TestClient with isolated test activities."""
    # Replace the global activities dict with test data for this test
    monkeypatch.setattr("src.app.activities", test_activities)
    return TestClient(app)
