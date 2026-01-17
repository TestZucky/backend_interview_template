"""Users feature tests."""
import pytest


def test_create_user_admin(client, admin_token):
    """Test creating a user as admin."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/users",
        json={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "password123",
            "role": "member"
        },
        headers=headers
    )
    
    assert response.status_code == 201
    assert response.json["success"] is True
    assert response.json["data"]["email"] == "jane@example.com"


def test_create_user_member_forbidden(client, member_token):
    """Test that members cannot create users."""
    headers = {"Authorization": f"Bearer {member_token}"}
    response = client.post(
        "/users",
        json={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "password123",
            "role": "member"
        },
        headers=headers
    )
    
    assert response.status_code == 403


def test_get_own_user(client, member_token, member_user_id):
    """Test member can view their own profile."""
    headers = {"Authorization": f"Bearer {member_token}"}
    response = client.get(f"/users/{member_user_id}", headers=headers)
    
    assert response.status_code == 200
    assert response.json["success"] is True


def test_get_other_user_forbidden(client, member_token, admin_user_id):
    """Test member cannot view other user's profile."""
    headers = {"Authorization": f"Bearer {member_token}"}
    response = client.get(f"/users/{admin_user_id}", headers=headers)
    
    assert response.status_code == 403


def test_list_users_admin(client, admin_token):
    """Test admin can list all users."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/users", headers=headers)
    
    assert response.status_code == 200
    assert response.json["success"] is True
    assert isinstance(response.json["data"], list)
