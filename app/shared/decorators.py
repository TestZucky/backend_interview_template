"""Shared decorators and utilities."""
from functools import wraps
from flask import request, jsonify


def validate_json(f):
    """Decorator to ensure request has JSON content type."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        return f(*args, **kwargs)
    return decorated_function
