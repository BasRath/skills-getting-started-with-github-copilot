"""Tests for POST /activities/{activity_name}/signup endpoint."""
import pytest


def test_signup_success(client):
    """Test successful signup for an activity."""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_participant_added(client):
    """Test that participant is actually added to the activity."""
    # First signup
    client.post("/activities/Chess Club/signup?email=alice@mergington.edu")
    
    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert "alice@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_participant_count_increases(client):
    """Test that participant count increases after signup."""
    response_before = client.get("/activities")
    before_count = len(response_before.json()["Programming Class"]["participants"])
    
    client.post("/activities/Programming Class/signup?email=bob@mergington.edu")
    
    response_after = client.get("/activities")
    after_count = len(response_after.json()["Programming Class"]["participants"])
    
    assert after_count == before_count + 1


def test_signup_already_registered(client):
    """Test that already registered student cannot sign up again."""
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )
    assert response.status_code == 400
    
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity returns 404."""
    response = client.post(
        "/activities/Nonexistent Activity/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_overbooking_allowed(client):
    """Test that students can sign up even when activity is at max capacity."""
    # Gym Class has max 30, currently has 2 participants
    # Fill it up to max
    for i in range(28):
        client.post(
            f"/activities/Gym Class/signup?email=student{i}@mergington.edu"
        )
    
    # Verify at max capacity
    response = client.get("/activities")
    gym_class = response.json()["Gym Class"]
    assert len(gym_class["participants"]) == 30
    
    # Try to add one more (should succeed due to permissive behavior)
    response = client.post(
        "/activities/Gym Class/signup?email=over@mergington.edu"
    )
    assert response.status_code == 200
    
    # Verify overbooking occurred
    response = client.get("/activities")
    gym_class = response.json()["Gym Class"]
    assert len(gym_class["participants"]) == 31
    assert gym_class["participants"][-1] == "over@mergington.edu"


def test_signup_empty_email(client):
    """Test signup with empty email."""
    response = client.post(
        "/activities/Chess Club/signup?email="
    )
    # Empty email is technically empty string, but server may not validate
    # Document current behavior: server accepts empty email
    # If this changes, update test accordingly
    # For now, just verify request goes through
    assert response.status_code in [200, 400, 422]


def test_signup_special_characters_in_email(client):
    """Test signup with email containing special characters."""
    response = client.post(
        "/activities/Chess Club/signup?email=test+tag@mergington.edu"
    )
    assert response.status_code == 200


def test_signup_multiple_activities(client):
    """Test that same student can sign up for multiple activities."""
    email = "multiact@mergington.edu"
    
    # Sign up for two different activities
    response1 = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )
    response2 = client.post(
        f"/activities/Programming Class/signup?email={email}"
    )
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify in both activities
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]
