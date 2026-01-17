# Backend Boilerplate

A production-ready backend template showcasing **clean architecture**, **separation of concerns**, and **best practices**.

## Project Structure

```
backend-boilerplate/
├── app/
│   ├── main.py                    # Flask app entry point
│   ├── db.py                      # Database configuration
│   ├── core/
│   │   ├── config.py              # Environment configuration
│   │   ├── auth.py                # JWT & password utilities
│   │   └── permissions.py         # Role-based access control
│   ├── features/
│   │   ├── auth/
│   │   │   ├── routes.py          # API endpoints
│   │   │   ├── resource.py        # Request/response schemas
│   │   │   ├── service.py         # Business logic
│   │   │   ├── model.py           # Database models
│   │   │   ├── utils.py           # Feature-specific utilities
│   │   │   ├── tests/
│   │   │   └── README.md
│   │   ├── users/
│   │   ├── clinics/
│   ├── shared/
│   │   ├── responses.py           # Common response formatting
│   │   ├── exceptions.py          # Custom exceptions
│   │   └── decorators.py          # Reusable decorators
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Architecture Pattern

Each feature is a **self-contained module** with:

- **Routes**: Flask blueprints handling HTTP requests
- **Resource**: Pydantic schemas for validation
- **Service**: Business logic and database operations
- **Model**: SQLAlchemy ORM models
- **Utils**: Feature-specific helpers
- **Tests**: Pytest test cases

This forces candidates to demonstrate:

- ✅ Layered thinking
- ✅ Separation of concerns
- ✅ Maintainable structure
- ✅ Clear abstractions

## Features

### 1. **Auth Feature**

- User registration (signup)
- User authentication (login)
- JWT token generation
- Role-based users (admin, member)

**Endpoints:**

- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login and get JWT token

### 2. **Users Feature**

- Admin onboarding/removal
- Member management
- Role assignment
- Profile management

**Endpoints:**

- `POST /users` - Create user (admin only)
- `GET /users` - List all users (admin only)
- `GET /users/<id>` - Get user profile (self or admin)
- `PATCH /users/<id>` - Update user (admin only)
- `DELETE /users/<id>` - Delete user (admin only)

### 3. **Clinics Feature**

- Clinic management
- Admin can manage clinics
- Members can view active clinics

**Endpoints:**

- `POST /clinics` - Create clinic (admin only)
- `GET /clinics` - List clinics (admin sees all, member sees active only)
- `GET /clinics/<id>` - Get clinic details
- `PATCH /clinics/<id>` - Update clinic (admin only)
- `DELETE /clinics/<id>` - Delete clinic (admin only)

## Getting Started

**⚡ For quick setup and testing, see [`SETUP.md`](./SETUP.md)**

For detailed development information, see [`QUICKSTART.md`](./QUICKSTART.md)

### Prerequisites

- Python 3.9+
- Poetry

### Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
poetry install
```

### Running the Application

```bash
source .venv/bin/activate
python -m flask --app app.main run --port 8000
```

The app will be available at `http://localhost:8000`

### Health Check

```bash
curl http://localhost:8000/health
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest app/features/auth/tests/test_auth.py
```

## Database Migrations with Alembic

This project uses **Alembic** for managing database schema changes. When you create new models or modify existing ones, follow these steps:

### First Time Setup

```bash
source .venv/bin/activate
poetry install  # Installs alembic
```

### Creating New Migrations

**After modifying or adding models:**

```bash
# Generate migration automatically (detects model changes)
alembic revision --autogenerate -m "Add new feature tables"

# Review the generated file in alembic/versions/
# Make manual adjustments if needed
```

### Applying Migrations

```bash
# Apply all pending migrations to database
alembic upgrade head

# Apply specific migration
alembic upgrade <revision_id>
```

### Reverting Migrations

```bash
# Rollback the last migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

### Checking Migration Status

```bash
# View current database revision
alembic current

# View all migrations and their status
alembic history --verbose
```

### Example Workflow - Adding a New Feature

```bash
# 1. Create new model
# File: app/features/yourfeature/model.py
# Include it in app/db.py Base.metadata

# 2. Generate migration
alembic revision --autogenerate -m "Add yourfeature tables"

# 3. Review and edit generated migration if needed
# File: alembic/versions/xxx_add_yourfeature_tables.py

# 4. Apply migration
alembic upgrade head

# 5. Run tests
pytest

# 6. If needed, rollback
alembic downgrade -1
```

### Migration File Structure

Each migration file in `alembic/versions/` contains:

```python
def upgrade() -> None:
    """Apply migration."""
    op.create_table(
        'new_table',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    """Revert migration."""
    op.drop_table('new_table')
```

## Adding New Features

### Step-by-Step Guide

#### 1. Create Feature Directory

```bash
mkdir -p app/features/yourfeature/tests
cd app/features/yourfeature
touch __init__.py model.py schemas.py resource.py service.py routes.py utils.py README.md
touch tests/__init__.py tests/test_yourfeature.py
```

#### 2. Create Database Model (`model.py`)

```python
"""Yourfeature models."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.db import Base

class YourModel(Base):
    """Your model description."""
    __tablename__ = "your_table_name"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
```

#### 3. Register Model in `app/db.py`

Add this import to the models section in `app/db.py`:

```python
from app.features.yourfeature.model import YourModel  # noqa: F401, E402
```

#### 4. Create Pydantic Schemas (`schemas.py`)

```python
"""Yourfeature request/response schemas."""
from pydantic import BaseModel, Field
from typing import Optional

class CreateYourFeatureRequestSchema(BaseModel):
    """Request schema for creating yourfeature."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)

class UpdateYourFeatureRequestSchema(BaseModel):
    """Request schema for updating yourfeature."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None
```

#### 5. Create Resource Mapping (`resource.py`)

```python
"""Yourfeature resource (response schemas and ORM mapping)."""
from pydantic import BaseModel
from datetime import datetime
from app.features.yourfeature.schemas import (
    CreateYourFeatureRequestSchema,
    UpdateYourFeatureRequestSchema
)

CreateYourFeatureRequest = CreateYourFeatureRequestSchema
UpdateYourFeatureRequest = UpdateYourFeatureRequestSchema

class YourFeatureResponse(BaseModel):
    """Response schema for yourfeature."""
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
```

#### 6. Create Business Logic (`service.py`)

```python
"""Yourfeature service (business logic)."""
from sqlalchemy.orm import Session
from app.features.yourfeature.model import YourModel
from app.shared.exceptions import NotFoundError

class YourFeatureService:
    """Service for yourfeature operations."""

    @staticmethod
    def create(db: Session, name: str, description: str = None) -> YourModel:
        """Create new yourfeature."""
        obj = YourModel(name=name, description=description)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_by_id(db: Session, obj_id: int) -> YourModel:
        """Get yourfeature by ID."""
        obj = db.query(YourModel).filter(YourModel.id == obj_id).first()
        if not obj:
            raise NotFoundError(f"Item {obj_id} not found")
        return obj
```

#### 7. Create API Endpoints (`routes.py`)

```python
"""Yourfeature routes (endpoints)."""
from flask import Blueprint, request
from sqlalchemy.orm import Session

from app.db import get_db
from app.core.permissions import require_role
from app.features.yourfeature.service import YourFeatureService
from app.features.yourfeature.resource import (
    CreateYourFeatureRequest,
    YourFeatureResponse
)
from app.shared.responses import success_response, error_response
from app.shared.decorators import validate_json
from app.shared.exceptions import AppException

yourfeature_bp = Blueprint("yourfeature", __name__, url_prefix="/yourfeature")

@yourfeature_bp.route("", methods=["POST"])
@validate_json
@require_role("admin")
def create():
    """Create new yourfeature (admin only)."""
    try:
        data = request.get_json()
        create_request = CreateYourFeatureRequest(**data)

        db = next(get_db())
        obj = YourFeatureService.create(db=db, name=create_request.name)

        response = YourFeatureResponse.from_orm(obj)
        return success_response(
            data=response.dict(),
            message="Created successfully",
            status_code=201
        )
    except AppException as e:
        return error_response(
            error=e.error_code,
            message=e.message,
            status_code=e.status_code
        )
```

#### 8. Register Blueprint in `app/main.py`

```python
from app.features.yourfeature.routes import yourfeature_bp

def create_app():
    # ... existing code ...
    app.register_blueprint(yourfeature_bp)
    return app
```

#### 9. Create Database Migration

```bash
source .venv/bin/activate

# Generate migration (Alembic detects new model)
alembic revision --autogenerate -m "Add yourfeature tables"

# Review generated migration
# alembic/versions/xxx_add_yourfeature_tables.py

# Apply migration
alembic upgrade head
```

#### 10. Create Tests (`tests/test_yourfeature.py`)

```python
"""Yourfeature feature tests."""
import pytest

def test_create_yourfeature(client, admin_token):
    """Test creating yourfeature."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/yourfeature",
        json={"name": "Test Item", "description": "Test"},
        headers=headers
    )

    assert response.status_code == 201
    assert response.json["success"] is True
```

#### 11. Create API Documentation (`README.md`)

Follow the OpenAI-style format from existing features.

---

### Complete Workflow Checklist

```bash
✅ Create feature directory structure
✅ Create model.py with SQLAlchemy models
✅ Register model in app/db.py
✅ Create schemas.py with Pydantic schemas
✅ Create resource.py with response mapping
✅ Create service.py with business logic
✅ Create routes.py with API endpoints
✅ Register blueprint in app/main.py
✅ Generate migration: alembic revision --autogenerate -m "..."
✅ Apply migration: alembic upgrade head
✅ Create tests in tests/test_yourfeature.py
✅ Create API documentation in README.md
✅ Run tests: pytest app/features/yourfeature/tests/
✅ Test manually with Postman or curl
```

## API Examples

### 1. Sign Up

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### 3. Access Protected Endpoint

```bash
curl -X GET http://localhost:8000/users/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Key Design Decisions

### 1. **Feature-Based Structure**

Each feature is independent, making it easy to add, modify, or remove functionality.

### 2. **Layered Architecture**

- **Routes**: HTTP handling
- **Resource**: Data validation
- **Service**: Business logic
- **Model**: Data persistence

### 3. **Shared Utilities**

Common functionality (responses, exceptions, decorators) is centralized.

### 4. **Permission System**

Role-based access control with decorators for clean, readable authorization.

### 5. **Error Handling**

Custom exceptions with consistent error responses.

## Extension Points

### Adding a New Feature

1. Create feature folder: `app/features/my_feature/`
2. Create files:
   - `model.py` - Database models
   - `resource.py` - Request/response schemas
   - `service.py` - Business logic
   - `routes.py` - API endpoints
   - `utils.py` - Feature-specific utilities
   - `tests/` - Test cases
   - `README.md` - Documentation

3. Register blueprint in `app/main.py`:

```python
from app.features.my_feature.routes import my_feature_bp
app.register_blueprint(my_feature_bp)
```

## Best Practices Demonstrated

✅ **Clean Code**: Clear, readable, well-organized code
✅ **Separation of Concerns**: Each component has a single responsibility
✅ **DRY Principle**: Shared utilities avoid duplication
✅ **Error Handling**: Custom exceptions with meaningful messages
✅ **Testing**: Comprehensive test coverage
✅ **Documentation**: Feature-level and code-level documentation
✅ **Security**: Password hashing, JWT tokens, role-based access
✅ **Scalability**: Modular structure allows easy feature additions

## Configuration

Environment variables:

- `ENVIRONMENT`: development | production | testing
- `DATABASE_URL`: Database connection string
- `JWT_SECRET`: Secret key for JWT signing
- `DEBUG`: Enable/disable debug mode
- `SQL_ECHO`: Log SQL queries

## Common Interview Questions This Template Addresses

1. **How do you structure a backend application?**
   - Feature-based, layered architecture

2. **How do you handle authorization?**
   - Custom decorators, role-based access control

3. **How do you validate user input?**
   - Pydantic schemas in resource layer

4. **How do you handle errors?**
   - Custom exceptions with consistent responses

5. **How do you write testable code?**
   - Dependency injection, service layer abstraction

6. **How do you organize business logic?**
   - Service layer handles all logic

7. **How do you reuse code?**
   - Shared utilities module

8. **How do you document code?**
   - README per feature, clear function signatures

## License

MIT License - Feel free to use and modify as needed.

## Questions?

Refer to individual feature READMEs for detailed documentation on each endpoint.
