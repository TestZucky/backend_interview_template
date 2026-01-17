"""Auth routes (endpoints)."""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session

from app.db import get_db
from app.features.auth.service import AuthService
from app.features.auth.resource import SignupRequest, LoginRequest, LoginResponse, UserResponse
from app.shared.responses import success_response, error_response
from app.shared.decorators import validate_json
from app.shared.exceptions import AppException

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/signup", methods=["POST"])
@validate_json
def signup():
    """User signup endpoint."""
    try:
        # Validate request
        data = request.get_json()
        signup_request = SignupRequest(**data)
        
        # Create user
        db = next(get_db())
        user = AuthService.signup(
            db=db,
            name=signup_request.name,
            email=signup_request.email,
            password=signup_request.password,
            role=signup_request.role,
        )
        
        # Return response
        user_response = UserResponse.from_orm(user)
        return success_response(
            data=user_response.dict(),
            message="User registered successfully",
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


@auth_bp.route("/login", methods=["POST"])
@validate_json
def login():
    """User login endpoint."""
    try:
        # Validate request
        data = request.get_json()
        login_request = LoginRequest(**data)
        
        # Authenticate user
        db = next(get_db())
        user, access_token = AuthService.login(
            db=db,
            email=login_request.email,
            password=login_request.password,
        )
        
        # Return response
        user_response = UserResponse.from_orm(user)
        login_response = LoginResponse(
            access_token=access_token,
            user=user_response
        )
        
        return success_response(
            data=login_response.dict(),
            message="Login successful",
            status_code=200
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
