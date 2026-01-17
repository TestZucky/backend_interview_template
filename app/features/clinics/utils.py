"""Clinics utility functions."""


def can_view_clinic(user_role: str) -> bool:
    """Check if user can view clinics."""
    return user_role in ["admin", "member"]


def can_manage_clinic(user_role: str) -> bool:
    """Check if user can manage clinics."""
    return user_role == "admin"
