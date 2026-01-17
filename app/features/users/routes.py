"""Users routes (endpoints)."""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session

from app.db import get_db
from app.core.permissions import get_current_user, require_role, require_any_role
from app.features.users.service import UsersService
from app.features.users.resource import CreateUserRequest, UpdateUserRequest, UserResponse
from app.features.users.utils import is_authorized_to_view_user
from app.shared.responses import success_response, error_response
from app.shared.decorators import validate_json
from app.shared.exceptions import AppException, ForbiddenError

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("", methods=["POST"])
@validate_json
@require_role("admin")
def create_user():
    """Create a new user (admin only)."""
    try:
        current_user = get_current_user()
        data = request.get_json()
        create_request = CreateUserRequest(**data)
        
        db = next(get_db())
        user = UsersService.create_user(
            db=db,
            name=create_request.name,
            email=create_request.email,
            password=create_request.password,
            role=create_request.role,
        )
        
        user_response = UserResponse.from_orm(user)
        return success_response(
            data=user_response.dict(),
            message="User created successfully",
            status_code=201
        )
    
    except AppException as e:
        return error_response(
            error=e.error_code,
            message=e.message,
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            error="INVALID_REQUEST",
            message=str(e),
            status_code=400
        )


@users_bp.route("/<int:user_id>", methods=["GET"])
@require_any_role(["admin", "member"])
def get_user(user_id: int):
    """Get user by ID."""
    try:
        current_user = get_current_user()
        
        # Check authorization
        if not is_authorized_to_view_user(int(current_user["sub"]), user_id, current_user["role"]):
            return error_response(
                error="FORBIDDEN",
                message="You don't have permission to view this user",
                status_code=403
            )
        
        db = next(get_db())
        user = UsersService.get_user(db, user_id)
        
        user_response = UserResponse.from_orm(user)
        return success_response(data=user_response.dict())
    
    except AppException as e:
        return error_response(
            error=e.error_code,
            message=e.message,
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            error="SERVER_ERROR",
            message=str(e),
            status_code=500
        )


@users_bp.route("", methods=["GET"])
@require_role("admin")
def list_users():
    """List all users (admin only)."""
    try:
        db = next(get_db())
        users = UsersService.list_users(db)
        
        users_response = [UserResponse.from_orm(user).dict() for user in users]
        return success_response(data=users_response)
    
    except Exception as e:
        return error_response(
            error="SERVER_ERROR",
            message=str(e),
            status_code=500
        )


@users_bp.route("/<int:user_id>", methods=["PATCH"])
@validate_json
@require_role("admin")
def update_user(user_id: int):
    """Update user information (admin only)."""
    try:
        data = request.get_json()
        update_request = UpdateUserRequest(**data)
        
        db = next(get_db())
        user = UsersService.update_user(
            db=db,
            user_id=user_id,
            name=update_request.name,
            role=update_request.role,
        )
        
        user_response = UserResponse.from_orm(user)
        return success_response(data=user_response.dict(), message="User updated successfully")
    
    except AppException as e:
        return error_response(
            error=e.error_code,
            message=e.message,
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            error="INVALID_REQUEST",
            message=str(e),
            status_code=400
        )


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@require_role("admin")
def delete_user(user_id: int):
    """Delete a user (admin only)."""
    try:
        db = next(get_db())
        UsersService.delete_user(db, user_id)
        
        return success_response(message="User deleted successfully")
    
    except AppException as e:
        return error_response(
            error=e.error_code,
            message=e.message,
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            error="SERVER_ERROR",
            message=str(e),
            status_code=500
        )
