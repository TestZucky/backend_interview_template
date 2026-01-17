"""Clinics feature tests."""
import pytest


def test_create_clinic_admin(client, admin_token):
    """Test creating a clinic as admin."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/clinics",
        json={
            "name": "City Medical Center",
            "address": "123 Main St, Springfield"
        },
        headers=headers
    )
    
    assert response.status_code == 201
    assert response.json["success"] is True
    assert response.json["data"]["name"] == "City Medical Center"


def test_create_clinic_member_forbidden(client, member_token):
    """Test that members cannot create clinics."""
    headers = {"Authorization": f"Bearer {member_token}"}
    response = client.post(
        "/clinics",
        json={
            "name": "City Medical Center",
            "address": "123 Main St, Springfield"
        },
        headers=headers
    )
    
    assert response.status_code == 403


def test_list_clinics_admin(client, admin_token):
    """Test admin can see all clinics."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create a clinic
    client.post(
        "/clinics",
        json={
            "name": "City Medical Center",
            "address": "123 Main St, Springfield"
        },
        headers=headers
    )
    
    # List clinics
    response = client.get("/clinics", headers=headers)
    
    assert response.status_code == 200
    assert response.json["success"] is True
    assert isinstance(response.json["data"], list)


def test_list_clinics_member_active_only(client, member_token, admin_token):
    """Test member can see only active clinics."""
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    member_headers = {"Authorization": f"Bearer {member_token}"}
    
    # Create an inactive clinic
    client.post(
        "/clinics",
        json={
            "name": "Inactive Clinic",
            "address": "456 Oak Ave"
        },
        headers=admin_headers
    )
    
    # Get clinic ID and make it inactive
    clinics_response = client.get("/clinics", headers=admin_headers)
    clinic_id = clinics_response.json["data"][-1]["id"]
    client.patch(
        f"/clinics/{clinic_id}",
        json={"is_active": False},
        headers=admin_headers
    )
    
    # Member should not see inactive clinic
    response = client.get("/clinics", headers=member_headers)
    clinic_names = [c["name"] for c in response.json["data"]]
    assert "Inactive Clinic" not in clinic_names
