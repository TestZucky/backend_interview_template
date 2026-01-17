"""Users utility functions."""


def is_authorized_to_view_user(current_user_id: int, target_user_id: int, current_user_role: str) -> bool:
    """Check if current user can view target user."""
    # Admin can view all users
    if current_user_role == "admin":
        return True
    
    # Member can only view themselves
    return current_user_id == target_user_id
