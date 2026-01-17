"""Custom application exceptions."""


class AppException(Exception):
    """Base application exception."""
    
    def __init__(self, message: str, status_code: int = 400, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        super().__init__(self.message)


class ValidationError(AppException):
    """Validation error."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=400, error_code="VALIDATION_ERROR")
        self.details = details


class NotFoundError(AppException):
    """Resource not found error."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, error_code="NOT_FOUND")


class UnauthorizedError(AppException):
    """Unauthorized error."""
    
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401, error_code="UNAUTHORIZED")


class ForbiddenError(AppException):
    """Forbidden error."""
    
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403, error_code="FORBIDDEN")


class ConflictError(AppException):
    """Conflict error (e.g., duplicate resource)."""
    
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, status_code=409, error_code="CONFLICT")
