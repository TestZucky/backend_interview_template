"""Permission and role checking utilities."""
from enum import Enum
from typing import List

from flask import request

from app.core.auth import decode_access_token


class Role(str, Enum):
    """User roles."""
    ADMIN = "admin"
    MEMBER = "member"


def get_current_user() -> dict:
    """Extract current user from JWT token in request headers."""
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header.split(" ")[1]
    return decode_access_token(token)


def require_auth(f):
    """Decorator to require authentication."""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_current_user()
        if not current_user:
            from flask import jsonify
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function


def require_role(required_role: str):
    """Decorator to require a specific role."""
    def decorator(f):
        from functools import wraps
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_current_user()
            if not current_user:
                from flask import jsonify
                return jsonify({"error": "Unauthorized"}), 401
            
            if current_user.get("role") != required_role:
                from flask import jsonify
                return jsonify({"error": "Forbidden"}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_any_role(required_roles: List[str]):
    """Decorator to require any of the specified roles."""
    def decorator(f):
        from functools import wraps
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_current_user()
            if not current_user:
                from flask import jsonify
                return jsonify({"error": "Unauthorized"}), 401
            
            if current_user.get("role") not in required_roles:
                from flask import jsonify
                return jsonify({"error": "Forbidden"}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
