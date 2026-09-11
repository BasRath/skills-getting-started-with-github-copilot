"""Tests for GET /activities endpoint."""
import pytest


def test_get_activities_success(client):
    """Test successful retrieval of all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_activities_structure(client):
    """Test that activities have correct structure."""
    response = client.get("/activities")
    data = response.json()
    
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_activities_content(client):
    """Test that activities contain correct data."""
    response = client.get("/activities")
    data = response.json()
    
    chess_club = data["Chess Club"]
    assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
    assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert chess_club["max_participants"] == 12
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_activities_json_serializable(client):
    """Test that response is valid JSON."""
    response = client.get("/activities")
    assert response.headers["content-type"] == "application/json"
    # If we got here without exception, JSON is valid
    response.json()
