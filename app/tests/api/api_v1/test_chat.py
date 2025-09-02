from fastapi.testclient import TestClient
from app.main import app
import pytest
from datetime import datetime

client = TestClient(app)

def test_create_session():
    response = client.post(
        "/api/v1/chat/sessions",
        json={"session_user": "testuser"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_user"] == "testuser"
    assert "session_id" in data
    assert "created_at" in data

def test_create_session_empty_username():
    response = client.post(
        "/api/v1/chat/sessions",
        json={"session_user": ""}
    )
    assert response.status_code == 400

def test_add_message():
    # First create a session
    session_response = client.post(
        "/api/v1/chat/sessions",
        json={"session_user": "testuser"}
    )
    session_id = session_response.json()["session_id"]
    
    # Add a message
    response = client.post(
        f"/api/v1/chat/sessions/{session_id}/messages",
        json={"role": "user", "content": "Hello"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "user"
    assert data["content"] == "Hello"

def test_get_messages():
    # First create a session
    session_response = client.post(
        "/api/v1/chat/sessions",
        json={"session_user": "testuser"}
    )
    session_id = session_response.json()["session_id"]
    
    # Add some messages
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    for message in messages:
        client.post(
            f"/api/v1/chat/sessions/{session_id}/messages",
            json=message
        )
    
    # Get all messages
    response = client.get(f"/api/v1/chat/sessions/{session_id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Test filtering by role
    response = client.get(f"/api/v1/chat/sessions/{session_id}/messages?role=user")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["role"] == "user"
