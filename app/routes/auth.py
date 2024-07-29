"""
app/routes/auth.py
This module contains the routes for the authentication endpoints.
It includes routes to authenticate a user and get the current user information.
"""

from fastapi import APIRouter, Depends, status, HTTPException
from app.models.token import Token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.operations.auth import user_dependency, login

router = APIRouter()

def get_db():
  """
  Returns a database session.
  """
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  """
  Authenticates the user and returns an access token.

  Attributes:
    form_data (OAuth2PasswordRequestForm): The user's login credentials.
    db (Session): The database session.

  Returns:
    Token: The access token.
  """
  return await login(form_data.username, form_data.password, db)


@router.get("/current_user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency):
  """
  Get the user information.

  Attributes:
    user (user_dependency): The user object.

  Returns:
    dict: A dictionary containing the user information.

  Raises:
    HTTPException: If authentication fails.
  """
  if user is None:
    return HTTPException(status_code=401, detail="Authentication failed")
  return {"user": user}