# Users Endpoint

The `app/routes/users.py` module defines the API routes for user-related operations in the application. It includes endpoints to create a user and retrieve user information by email. 

## Endpoints

### 1. `/users/` (POST)
This endpoint creates a new user in the database.

#### Request
- **Method**: POST
- **Path**: `/users/`
- **Request Body**: 
  - `email` (string): The user's email address.
  - `name` (string): The user's name.
  - `mobile_number` (string): The user's mobile number.
  - `password` (string): The user's password.

## Response:
- **Success (200 OK)**: 
    - Returns the created user object.
- **Error (400 Bad Request)**: 
    - If the email is already registered.

#### Example
```sh
curl -X POST "http://localhost:8000/users/" 
     -H "Content-Type: application/json" 
     -d {
            "email": "string",
            "name": "string",
            "mobile_number": "string",
            "password": "string"
        }
```

#### Request Example
```json
{
    "email": "testuser@example.com",
    "name": "Test User",
    "mobile_number": "1234567890",
    "password": "testpassword"
}
```

### 2. `/users/{email}` (GET)
This endpoint retrieves a user by their email.

#### Request
- **Method**: GET
- **Path**: `/users/{email}`
- **Request Body**: 
    - `email` (str): The email of the user.

#### Responses
- **Success (200 OK)**: 
    - Returns the user object.
- **Error (404 Not Found)**: 
    - If the user with the specified email is not found.

#### Example
```sh
curl -X POST "http://localhost:8000/users/testuser@example.com"
```

#### Responses Example
```json
{
    "email": "testuser@example.com",
    "name": "Test User",
    "mobile_number": "1234567890"
    "id" : 1
}
```

## Dependencies

The module relies on several dependencies to function correctly:

- **FastAPI**: The web framework used to create the API routes.
- **SQLAlchemy**: The ORM used for database operations.
- **app.operations**: Contains the business logic for creating and retrieving users.
- **app.schemas**: Defines the data models and validation using Pydantic.
- **app.database**: Provides the database session.
- **app.operations.auth**: Provides user authentication dependencies.