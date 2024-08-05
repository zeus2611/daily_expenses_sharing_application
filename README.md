# Daily Expenses Sharing Application

## Overview

The Daily Expenses Sharing Application is designed to help users track and share their daily expenses. Users can create accounts, log expenses, and share them with other participants. The application ensures data validation, error handling, and provides a RESTful API for ease of use.

## Features

- User Registration
- Authentication and Authorization
- Expense Tracking
- Sharing Expenses with Participants
- Comprehensive API Documentation

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [API Endpoints](#api-endpoints)
4. [Models](#models)
5. [Error Handling](#error-handling)
6. [Validation](#validation)

## Installation

### Prerequisites

- Python 3.9 or higher
- FastAPI
- SQLAlchemy
- SQLite (or any other preferred database)
- Pydantic

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/zeus2611/daily_expenses_sharing_application.git
    ```

2. Navigate to the project directory:

    ```bash
    cd daily_expenses_sharing_application
    ```

3. Install the required dependencies:

    ```bash
    python3 -m venv venv 
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    uvicorn app.main:app --reload
    ```

## Usage

### Running the Server

After installation, start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

### Accessing API Documentation

Open your browser and navigate to:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Running the tests

After installation, we can run the tests:
```bash
pytest tests/
```

## API Endpoints

- [**Authentication Endpoint**](docs/routes/auth.md) - This module contains the endpoints for authentication and authorization.

- [**User Endpoints**](docs/routes/users.md) - This module contains the endpoints for user management.

- [**Expense Endpoints**](docs/routes/expenses.md) - This module contains the endpoints for expense management.

## Models

### User Model

- **UserBase**

    ```python
    class UserBase(BaseModel):
        email: EmailStr
        name: str
        mobile_number: Annotated[str, Field(min_length=10, max_length=10, regex=r'^\d{10}$')]
    ```

- **UserCreate**

    ```python
    class UserCreate(UserBase):
        pass
    ```

- **User**

    ```python
    class User(UserBase):
        id: int

        class Config:
            orm_mode = True
    ```

### Expense Model

- **ExpenseBase**

    ```python
    class ExpenseBase(BaseModel):
        title: str
        total_amount: float
    ```

- **ExpenseCreate**

    ```python
    class ExpenseCreate(ExpenseBase):
        participants: List[Participant]
    ```

- **Expense**

    ```python
    class Expense(ExpenseBase):
        id: int
        participants: List[Participant]

        class Config:
            orm_mode = True
    ```

### Participant Model

- **Participant**

    ```python
    class Participant(BaseModel):
        name: str
        amount: float
        percentage: float
    ```

## Error Handling

The application includes comprehensive error handling to manage validation and database errors.

### Validation Error Handling

Validation errors are captured and returned as a `422 Unprocessable Entity` response:

```python
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

### Unique Constraint Error Handling

Unique constraint violations (e.g., duplicate email) are managed and returned as a `400 Bad Request` response:

```python
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Otherwise create user
```

### Split Type Error Handling

#### Total Percentage Integrity Error

Ensure the total percentage of all participants in an expense adds up to 100%. If it doesn't, raise a `400 Bad Request` error.

**Implementation**

We have a validator module with function to ensure that the percentage over all participant is equal to 100.

- Function for percentage integrity check:

```python
def total_percentage(expense: ExpenseCreate):
    return sum([p.percentage for p in expense.participants]) == 100
```

- We can use this validator function while creating the participant share.
```python
def split_percentage(db: Session, db_expense: Expense, expense: ExpenseCreate):
    if not total_percentage(expense):
        msg="The total percentage of participants must be 100%"
        raise ExpenseValidationError(name="TotalPercentageError", message=msg)
    # Otherwise we can continue to create the paricipants share.
```

**Error Response**:

```json
{
  "detail": "Total percentage of participants must equal 100"
}
```

#### Total Amount Integrity Error

Ensure the total amount specified is equal to the sum of the amounts for each participant. If not, raise a `400 Bad Request` error.

**Implementation**

We have a validator module with function to ensure that the percentage over all participant is equal to 100.

- Function for percentage integrity check:

```python
def total_amount(expense: ExpenseCreate):
    return sum([p.amount for p in expense.participants]) == expense.total_amount
```

- We can use this validator function while creating the participant share.
```python
def split_exact(db: Session, db_expense: Expense, expense: ExpenseCreate):
    if not total_amount(expense):
        raise ExpenseValidationError(
            name="TotalAmountError",
            message="The total amount distributed among participants must equal the total expense amount"
            )
    # Otherwise we can continue to create the paricipants share.
```

**Error Response**:

```json
{
  "detail": "Total amount must equal the sum of participant amounts"
}
```

## Validation

The application uses Pydantic models for data validation to ensure data integrity and prevent invalid data from being processed.

### Email Validation

Emails are validated using Pydantic's `EmailStr` type:

```python
email: EmailStr
```

### Mobile Number Validation

Mobile numbers are validated to ensure they are exactly 10 digits long:

```python
mobile_number: Annotated[str, Field(min_length=10, max_length=10, regex=r'^\d{10}$')]
```

