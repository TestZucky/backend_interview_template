# Users Feature - API Documentation

## Overview
User management system for administrators. Admins can create, read, update, and delete users. Members can only view their own profile. All endpoints require authentication.

---

## POST /users
Create a new user (Admin Only).

### Description
Admin-only endpoint to create new users. Users are created with specified role (admin or member).

### Authorization
- **Required**: Admin role
- **Header**: `Authorization: Bearer {token}`

### Request Body
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "password": "password123",
  "role": "member"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | User's full name (1-255 chars) |
| `email` | string | ✓ | Valid email address (must be unique) |
| `password` | string | ✓ | Password (minimum 6 characters) |
| `role` | string | ✓ | User role: "admin" or "member" |

### Response
**Status: 201 Created**
```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "id": 2,
    "name": "Jane Doe",
    "email": "jane@example.com",
    "role": "member",
    "created_at": "2024-01-17T10:00:00"
  }
}
```

---

## GET /users
List all users (Admin Only).

### Description
Retrieve all users in the system. Admin-only endpoint.

### Authorization
- **Required**: Admin role
- **Header**: `Authorization: Bearer {token}`

### Response
**Status: 200 OK**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "role": "admin",
      "created_at": "2024-01-17T10:00:00"
    }
  ]
}
```

---

## GET /users/{id}
Get user by ID.

### Description
Get specific user details. Members can only view their own profile, admins can view any user.

### Authorization
- **Required**: Authenticated (Member or Admin)
- **Header**: `Authorization: Bearer {token}`

### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | User ID |

### Response
**Status: 200 OK**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "admin",
    "created_at": "2024-01-17T10:00:00"
  }
}
```

### Error Responses
**Status: 403 Forbidden** - Not authorized
```json
{
  "success": false,
  "error": "FORBIDDEN",
  "message": "You don't have permission to view this user"
}
```

---

## PATCH /users/{id}
Update user (Admin Only).

### Description
Update user information. Admin-only endpoint.

### Authorization
- **Required**: Admin role
- **Header**: `Authorization: Bearer {token}`

### Request Body
```json
{
  "name": "John Updated",
  "role": "admin"
}
```

### Response
**Status: 200 OK**
```json
{
  "success": true,
  "message": "User updated successfully",
  "data": {
    "id": 1,
    "name": "John Updated",
    "role": "admin",
    "created_at": "2024-01-17T10:00:00"
  }
}
```

---

## DELETE /users/{id}
Delete user (Admin Only).

### Description
Remove user from system. Admin-only endpoint.

### Authorization
- **Required**: Admin role
- **Header**: `Authorization: Bearer {token}`

### Response
**Status: 200 OK**
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

---

## Authorization Rules

| Endpoint | Method | Required Role | Notes |
|----------|--------|---------------|-------|
| `/users` | GET | Admin | List all users |
| `/users` | POST | Admin | Create new user |
| `/users/{id}` | GET | Member/Admin | Self-view or Admin |
| `/users/{id}` | PATCH | Admin | Update user info |
| `/users/{id}` | DELETE | Admin | Delete user |

---

## Code Structure
```
users/
├── routes.py      # API endpoints
├── resource.py    # Pydantic schemas
├── service.py     # Business logic
├── utils.py       # Utilities
└── tests/         # Unit tests
```
