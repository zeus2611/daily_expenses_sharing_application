"""
app/routes/users.py
This module contains the routes for the users.
It includes routes to create a user and get a user by ID.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import operations, schemas
from ..database import SessionLocal
from app.operations.auth import user_dependency

router = APIRouter()

def get_db():
    """
    Create a new database session for each request.

    Returns:
        Session: The database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a user in the database.

    Attributes:
        user (UserCreate): The user details.
        db (Session): The database session.

    Returns:
        User: The created user.
    """
    return operations.create_user(db, user)

@router.get("/{email}", response_model=schemas.User)
def get_user(user: user_dependency, email: str, db: Session = Depends(get_db)):
    """
    Get a user by ID.

    Attributes:
        email (str): The email of the user.
        db (Session): The database session.

    Returns:
        User: The user with the specified ID.
    """
    db_user = operations.get_user(user, db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
