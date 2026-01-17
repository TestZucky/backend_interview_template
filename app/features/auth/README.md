# Auth Feature - API Documentation

## Overview

User authentication and registration system with JWT token-based access control. Supports user signup, login, and role-based authorization (admin, member).

---

## POST /auth/signup

Register a new user account.

### Description

Creates a new user with specified role (defaults to member). Passwords are hashed using bcrypt for security.

### Request Body

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "member"
}
```

| Field      | Type   | Required | Description                                        |
| ---------- | ------ | -------- | -------------------------------------------------- |
| `name`     | string | ✓        | User's full name (1-255 chars)                     |
| `email`    | string | ✓        | Valid email address (must be unique)               |
| `password` | string | ✓        | Password (minimum 6 characters)                    |
| `role`     | string | ✗        | User role: "admin" or "member" (default: "member") |

### Response

**Status: 201 Created**

```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "member",
    "created_at": "2024-01-17T10:00:00"
  }
}
```

### Error Responses

**Status: 409 Conflict** - Email already exists

```json
{
  "success": false,
  "error": "CONFLICT",
  "message": "User with email john@example.com already exists"
}
```

**Status: 400 Bad Request** - Invalid role

```json
{
  "success": false,
  "error": "INVALID_REQUEST",
  "message": "Input should be 'admin' or 'member' [type=enum, input_value='superuser', input_type=str]"
}
```

### Examples

**Signup as member (default):**

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Signup as admin:**

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin User",
    "email": "admin@example.com",
    "password": "password123",
    "role": "admin"
  }'
```

---

## POST /auth/login

Authenticate user and obtain JWT access token.

### Description

Validates email and password. Returns JWT token valid for 24 hours. Token must be included in Authorization header for protected endpoints.

### Request Body

```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

| Field      | Type   | Required | Description          |
| ---------- | ------ | -------- | -------------------- |
| `email`    | string | ✓        | User's email address |
| `password` | string | ✓        | User's password      |

### Response

**Status: 200 OK**

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "role": "member",
      "created_at": "2024-01-17T10:00:00"
    }
  }
}
```

### Error Responses

**Status: 401 Unauthorized** - Invalid credentials

```json
{
  "success": false,
  "error": "UNAUTHORIZED",
  "message": "Invalid email or password"
}
```

---

## Authentication

### Using the JWT Token

Include the access token in the Authorization header for protected endpoints:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Token Details

- **Format**: JWT (JSON Web Token)
- **Algorithm**: HS256
- **Expiration**: 24 hours from issue

---

## Database Schema

### User Table

| Column       | Type     | Constraints      | Description                |
| ------------ | -------- | ---------------- | -------------------------- |
| `id`         | Integer  | Primary Key      | Unique identifier          |
| `name`       | String   | NOT NULL         | User's full name           |
| `email`      | String   | UNIQUE, NOT NULL | Email (unique constraint)  |
| `password`   | String   | NOT NULL         | Bcrypt hashed password     |
| `role`       | Enum     | DEFAULT 'member' | User role (admin/member)   |
| `created_at` | DateTime | DEFAULT NOW      | Account creation timestamp |
