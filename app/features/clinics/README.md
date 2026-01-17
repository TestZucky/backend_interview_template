# Clinics Feature - API Documentation

## Overview
Clinic management system for healthcare facilities. Admins can manage (create, read, update, delete) clinics. Members can view only active clinics. All endpoints require authentication.

---

## POST /clinics
Create a new clinic (Admin Only).

### Description
Admin-only endpoint to create new clinic records. Clinics are active by default.

### Authorization
- **Required**: Admin role
- **Header**: `Authorization: Bearer {token}`

### Request Body
```json
{
  "name": "City Medical Center",
  "address": "123 Main St, Springfield"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | Clinic name (1-255 chars) |
| `address` | string | ✓ | Full address (1-500 chars) |

### Response
**Status: 201 Created**
```json
{
  "success": true,
  "message": "Clinic created successfully",
  "data": {
    "id": 1,
    "name": "City Medical Center",
    "address": "123 Main St, Springfield",
    "is_active": true,
    "created_at": "2024-01-17T10:00:00"
  }
}
```

### Error Response
**Status: 403 Forbidden** - Not admin
```json
{
  "success": false,
  "error": "FORBIDDEN",
  "message": "You don't have permission to access this resource"
}
```

---

## GET /clinics
List clinics.

### Description
List all clinics. Admins see all clinics (active + inactive). Members see only active clinics.

### Authorization
- **Required**: Authenticated (Member or Admin)
- **Header**: `Authorization: Bearer {token}`

### Query Parameters
None

### Response
**Status: 200 OK**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "City Medical Center",
      "address": "123 Main St, Springfield",
      "is_active": true,
      "created_at": "2024-01-17T10:00:00"
    },
    {
      "id": 2,
      "name": "Suburban Clinic",
      "address": "456 Oak Ave, Springfield",
      "is_active": true,
      "created_at": "2024-01-17T10:00:00"
    }
  ]
}
```

### Visibility Rules
- **Admin**: Sees all clinics
- **Member**: Sees only active clinics (is_active = true)

---

## GET /clinics/{id}
Get clinic by ID.

### Description
Retrieve specific clinic details. Available to both members and admins.

### Authorization
- **Required**: Authenticated (Member or Admin)
- **Header**: `Authorization: Bearer {token}`

### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Clinic ID |

### Response
**Status: 200 OK**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "City Medical Center",
    "address": "123 Main St, Springfield",
    "is_active": true,
    "created_at": "2024-01-17T10:00:00"
  }
}
```

### Error Responses
**Status: 404 Not Found** - Clinic not found
```json
{
  "success": false,
  "error": "NOT_FOUND",
  "message": "Clinic 999 not found"
}
```

---

## PATCH /clinics/{id}
Update clinic (Admin Only).

### Description
Update clinic information. Admin-only endpoint. Can update name, address, or active status.

### Authorization
- **Required**: Admin role
- **Header**: `Authorization: Bearer {token}`

### Request Body
```json
{
  "name": "Updated Clinic Name",
  "address": "789 New St, Springfield",
  "is_active": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✗ | New clinic name |
| `address` | string | ✗ | New address |
| `is_active` | boolean | ✗ | Active status |

### Response
**Status: 200 OK**
```json
{
  "success": true,
  "message": "Clinic updated successfully",
  "data": {
    "id": 1,
    "name": "Updated Clinic Name",
    "address": "789 New St, Springfield",
    "is_active": true,
    "created_at": "2024-01-17T10:00:00"
  }
}
```

---

## DELETE /clinics/{id}
Delete clinic (Admin Only).

### Description
Remove clinic from system. Admin-only endpoint.

### Authorization
- **Required**: Admin role
- **Header**: `Authorization: Bearer {token}`

### Response
**Status: 200 OK**
```json
{
  "success": true,
  "message": "Clinic deleted successfully"
}
```

### Error Response
**Status: 404 Not Found** - Clinic not found
```json
{
  "success": false,
  "error": "NOT_FOUND",
  "message": "Clinic 999 not found"
}
```

---

## Database Schema

### Clinic Table
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key | Unique identifier |
| `name` | String | NOT NULL | Clinic name |
| `address` | String | NOT NULL | Full address |
| `is_active` | Boolean | DEFAULT TRUE | Active status |
| `created_at` | DateTime | DEFAULT NOW | Creation timestamp |

---

## Authorization & Visibility

### Endpoint Access
| Endpoint | Method | Required Role |
|----------|--------|---------------|
| `/clinics` | GET | Member/Admin |
| `/clinics` | POST | Admin |
| `/clinics/{id}` | GET | Member/Admin |
| `/clinics/{id}` | PATCH | Admin |
| `/clinics/{id}` | DELETE | Admin |

### Data Visibility
- **Admins**: Can see all clinics (active and inactive)
- **Members**: Can only see active clinics (is_active = true)

---

## Examples

### Admin views all clinics
```bash
curl -X GET http://localhost:8000/clinics \
  -H "Authorization: Bearer {admin_token}"
```

### Member views only active clinics
```bash
curl -X GET http://localhost:8000/clinics \
  -H "Authorization: Bearer {member_token}"
```

### Deactivate a clinic
```bash
curl -X PATCH http://localhost:8000/clinics/1 \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'
```

---

## Code Structure
```
clinics/
├── routes.py      # API endpoints
├── resource.py    # Pydantic schemas
├── service.py     # Business logic
├── model.py       # Database model
├── utils.py       # Utilities
└── tests/         # Unit tests
```
