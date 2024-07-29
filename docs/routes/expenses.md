# Expenses Endpoints

The `app/routes/expenses.py` module contains the routes for the expenses endpoints. It includes routes for managing expenses, including creating, retrieving, and downloading balance sheets.

## Endpoints

### 1. `/expenses/` (POST)
This endpoint creates an expense.

#### Request
- **Method**: POST
- **Path**: `/expenses/`
- **Request Body**: 
  - `description` (string): The expense's description.
  - `total_amount` (integer): The expense's total amount.
  - `date` (string): The expense's date .
  - `split_type` (string): The expense's split type among participants.
  - `creator_id` (integer): The expense's owner/creator id.
  - `participants` (list): The expense's participants.
    - `user_id` (integer): The participant's id.
    - `amount` (integer, Optional): The participant's share amount in total amount.
    - `percentage` (integer, Optional): The participant's share percentage of total amount.

#### Response
- **Success (200 OK)**:
  - Returns a `json` object containing the expense details.
- **Error (400 Bad Request)**:
  - Returns an error message if expense creation fails.

#### Example
```sh
curl -X 'POST' \
  'https://localhost:8000/expenses/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer `access_token`' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "string",
  "total_amount": 1,
  "date": "2024-07-29",
  "split_type": "EQUAL",
  "creator_id": 1,
  "participants": [
    {
      "user_id": 1
    }
  ]
}'
```

#### Response Example
```json
{
  "description": "string",
  "total_amount": 1,
  "date": "2024-07-29",
  "split_type": "EQUAL",
  "creator_id": 1,
  "participants": [
    {
      "user_id": 1,
      "amount": 1,
      "percentage": null,
      "id": 3,
      "expense_id": 4
    }
  ],
  "id": 4,
  "creator": {
    "email": "user@example.com",
    "name": "string",
    "mobile_number": "7784462176",
    "id": 1
  }
}
```

### 2. `/expenses/{expense_id}` (GET)
This endpoint fetches details of an expense.

#### Request
- **Method**: GET
- **Path**: `/expenses/{expense_id}`

#### Response
- **Success (200 OK)**:
  - Returns a `json` object containing the expense details.
- **Error (401 Unauthorized)**:
  - Returns an error message if expense details cannot be fetched.

#### Example
```sh
curl -X 'GET' \
  'https://localhost:8000/expenses/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer `access_token`'
```

#### Response Example
```json
{
  "description": "string",
  "total_amount": 10,
  "date": "2024-07-29",
  "split_type": "EQUAL",
  "creator_id": 1,
  "participants": [
    {
      "user_id": 1,
      "amount": 10,
      "percentage": null,
      "id": 1,
      "expense_id": 1
    }
  ],
  "id": 1,
  "creator": {
    "email": "user@example.com",
    "name": "string",
    "mobile_number": "7784462176",
    "id": 1
  }
}
```

### 3. `/expenses/user` (GET)
This endpoint fetches list of all expenses of a user.

#### Request
- **Method**: GET
- **Path**: `/expenses/user`

#### Response
- **Success (200 OK)**:
  - Returns a `json` object containing the all expense of a user.
- **Error (401 Unauthorized)**:
  - Returns an error message indicating user not authenticated.

#### Example
```sh
curl -X 'GET' \
  'https://localhost:8000/expenses/user' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer `access_token`'
```

#### Response Example
```json
[
  {
    "user_id": 1,
    "amount": 10,
    "percentage": null,
    "id": 1,
    "expense_id": 1
  }
]
```

### 4. `/expenses/balance-sheet` (GET)
This endpoint fetches the balance sheet as a downloadable file(CSV) containing all the expense details.

#### Request
- **Method**: GET
- **Path**: `/expenses/balance-sheet`

#### Response
- **Success (200 OK)**:
  - Returns a CSV downloadable file containg all expense details.

#### Example
```sh
curl -X 'GET' \
  'https://localhost:8000/expenses/balance-sheet/' \
  -H 'accept: application/json' 
```

## Dependencies

- `List`, `Depends`, `HTTPException`, `APIRouter` from FastAPI
- `Session` from SQLAlchemy ORM
- `StreamingResponse` from FastAPI responses
- Custom modules and functions: `operations`, `schemas`, `SessionLocal`, `user_dependency` from the application