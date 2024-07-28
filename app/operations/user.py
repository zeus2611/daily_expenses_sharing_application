"""
app/operations/user.py
This file contains the operations related to the user model.
It includes functions to create a user and get a user by ID.
For creating a user, the function checks if the email is 
already registered as email must be unique for each user.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models
from app.schemas import UserCreate
from app.utils.password import hash_password

def create_user(db: Session, user: UserCreate):
    """
    Create a user in the database.

    Attributes:
        db (Session): The database session.
        user (UserCreate): The user details.

    Returns:
        User: The created user.
    """

    # Check if the email is already registered. Email must be unique for each user.
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    # Create a new user in the database. If the email is not already registered, the user is created successfully.
    user = models.User(email=user.email, name=user.name, mobile_number=user.mobile_number, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

    

def get_user(db: Session, email: str):
    """
    Get a user by ID.

    Attributes:
        db (Session): The database session.
        email (str): The email of the user.

    Returns:
        User: The user with the specified ID.
    """
    return db.query(models.User).filter(models.User.email == email).first()
