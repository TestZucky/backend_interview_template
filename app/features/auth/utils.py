"""Auth utility functions."""
from pydantic import ValidationError as PydanticValidationError


def validate_request(schema_class, data):
    """Validate request data against schema."""
    try:
        return schema_class(**data)
    except PydanticValidationError as e:
        errors = {}
        for error in e.errors():
            field = ".".join(str(x) for x in error["loc"])
            errors[field] = error["msg"]
        raise ValueError(f"Validation failed: {errors}")
