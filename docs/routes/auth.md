# Authentication Endpoints

The `app/routes/auth.py` module contains the routes for the authentication endpoints. It includes routes to authenticate a user and get the current user information.

## Endpoints

### 1. `/token` (POST)
This endpoint authenticates a user and returns an access token.

#### Request
- **Method**: POST
- **Path**: `/token`
- **Request Body**: 
  - `username` (string): The user's email address.
  - `password` (string): The user's password.

#### Response
- **Success (200 OK)**:
  - Returns a `Token` object containing the access token.
- **Error (401 Unauthorized)**:
  - Returns an error message if authentication fails.

#### Example
```sh
curl -X POST "http://localhost:8000/token" 
     -H "Content-Type: application/x-www-form-urlencoded" 
     -d "username=testuser@example.com&password=testpassword"
```

#### Response Example
```json
{
  "access_token": "someaccesstoken",
  "token_type": "bearer"
}
```
### 2. `/current_user` (GET)
This endpoint retrieves the current user information.

#### Request
- **Method**: GET
- **Path**: /current_user
- **Headers**:
    - Authorization: Bearer token obtained from the `/token` endpoint.

#### Response
- **Success (200 OK)**:
    - Returns a `dictionary` containing the user information.
- **Error (401 Unauthorized)**:
    - Returns an error message if authentication fails.

#### Example
```sh
curl -X GET "http://localhost:8000/current_user" 
     -H "Authorization: Bearer `access_token`"
```

#### Response Example
```json
{
  "user": {
    "id": 1,
    "email": "testuser@example.com",
    "name": "Test User",
    "mobile_number": "1234567890"
  }
}
```

## Dependencies
The module depends on the following:

- **FastAPI**: Web framework for building the API.
- **SQLAlchemy**: ORM for interacting with the database.
- **OAuth2PasswordBearer** and **OAuth2PasswordRequestForm**: For handling authentication.
- **SessionLocal**: Database session dependency.
- **user_dependency** and **login** from app.operations.auth: Custom authentication operations.

## Functions
- `get_db()`:

    This function returns a new database session for each request. It ensures that the database session is properly closed after the request is handled.

- `login_for_access_token`(form_data: OAuth2PasswordRequestForm, db: Session):

    This function handles user authentication and returns an access token. It uses the login function from app.operations.auth to validate the user's credentials.

- `get_user(user: user_dependency)`:
    This function retrieves the current user's information using the user_dependency from app.operations.auth. If the user is not authenticated, it raises an HTTPException.
