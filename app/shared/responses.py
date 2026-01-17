"""Shared response utilities."""
from flask import jsonify
from typing import Any, Dict, Optional


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200
) -> tuple:
    """Return a success response."""
    response = {
        "success": True,
        "message": message,
        "data": data,
    }
    return jsonify(response), status_code


def error_response(
    error: str,
    message: str = None,
    status_code: int = 400,
    details: Optional[Dict] = None
) -> tuple:
    """Return an error response."""
    response = {
        "success": False,
        "error": error,
        "message": message or error,
    }
    if details:
        response["details"] = details
    return jsonify(response), status_code
