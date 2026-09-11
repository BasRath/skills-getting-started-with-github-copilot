"""Tests for DELETE /activities/{activity_name}/remove endpoint."""
import pytest


def test_remove_participant_success(client):
    """Test successful removal of a participant."""
    response = client.delete(
        "/activities/Chess Club/remove?email=michael@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "Removed" in data["message"]


def test_remove_participant_actually_removed(client):
    """Test that participant is actually removed from the activity."""
    # Remove a participant
    client.delete(
        "/activities/Chess Club/remove?email=michael@mergington.edu"
    )
    
    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_remove_participant_count_decreases(client):
    """Test that participant count decreases after removal."""
    response_before = client.get("/activities")
    before_count = len(response_before.json()["Chess Club"]["participants"])
    
    client.delete(
        "/activities/Chess Club/remove?email=michael@mergington.edu"
    )
    
    response_after = client.get("/activities")
    after_count = len(response_after.json()["Chess Club"]["participants"])
    
    assert after_count == before_count - 1


def test_remove_participant_not_signed_up(client):
    """Test removal of student who is not signed up returns 400."""
    response = client.delete(
        "/activities/Chess Club/remove?email=nosuchstudent@mergington.edu"
    )
    assert response.status_code == 400
    
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_remove_activity_not_found(client):
    """Test removal from non-existent activity returns 404."""
    response = client.delete(
        "/activities/Nonexistent Activity/remove?email=michael@mergington.edu"
    )
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_remove_last_participant(client):
    """Test removing the last participant from an activity."""
    # Programming Class has 2 participants, remove both
    client.delete(
        "/activities/Programming Class/remove?email=emma@mergington.edu"
    )
    client.delete(
        "/activities/Programming Class/remove?email=sophia@mergington.edu"
    )
    
    # Verify activity has no participants
    response = client.get("/activities")
    activities = response.json()
    assert len(activities["Programming Class"]["participants"]) == 0


def test_remove_and_signup_again(client):
    """Test that removed participant can sign up again."""
    email = "michael@mergington.edu"
    
    # Remove participant
    client.delete(f"/activities/Chess Club/remove?email={email}")
    
    # Verify removed
    response = client.get("/activities")
    assert email not in response.json()["Chess Club"]["participants"]
    
    # Sign up again
    response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )
    assert response.status_code == 200
    
    # Verify signed up
    response = client.get("/activities")
    assert email in response.json()["Chess Club"]["participants"]


def test_remove_participant_case_sensitive(client):
    """Test that email matching is case-sensitive (or document actual behavior)."""
    # Current implementation likely uses exact match
    response = client.delete(
        "/activities/Chess Club/remove?email=MICHAEL@MERGINGTON.EDU"
    )
    # If case-sensitive, this should fail
    assert response.status_code == 400


def test_remove_multiple_participants_sequentially(client):
    """Test removing multiple participants one by one."""
    email1 = "michael@mergington.edu"
    email2 = "daniel@mergington.edu"
    
    # Chess Club has these two
    response1 = client.delete(f"/activities/Chess Club/remove?email={email1}")
    response2 = client.delete(f"/activities/Chess Club/remove?email={email2}")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify both removed
    response = client.get("/activities")
    activities = response.json()
    assert len(activities["Chess Club"]["participants"]) == 0
