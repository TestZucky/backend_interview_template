"""Auth feature tests."""
import pytest
from app.features.auth.model import User
from app.core.permissions import Role


def test_signup_success(client, db):
    """Test successful user signup."""
    response = client.post("/auth/signup", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 201
    assert response.json["success"] is True
    assert response.json["data"]["email"] == "john@example.com"
    assert response.json["data"]["role"] == "member"


def test_signup_duplicate_email(client, db):
    """Test signup with duplicate email."""
    # Create first user
    client.post("/auth/signup", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    })
    
    # Try to create another with same email
    response = client.post("/auth/signup", json={
        "name": "Jane Doe",
        "email": "john@example.com",
        "password": "password456"
    })
    
    assert response.status_code == 409
    assert response.json["success"] is False


def test_login_success(client, db):
    """Test successful login."""
    # Register user
    client.post("/auth/signup", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    })
    
    # Login
    response = client.post("/auth/login", json={
        "email": "john@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "access_token" in response.json["data"]
    assert response.json["data"]["user"]["email"] == "john@example.com"


def test_login_invalid_credentials(client, db):
    """Test login with invalid credentials."""
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 401
    assert response.json["success"] is False
