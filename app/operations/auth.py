"""
app/operations/auth.py
This module contains the operations related to authentication.
It includes functions to authenticate a user, create an access token,
and get the current user.
"""

from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from app.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.token import Token
from app.utils.password import verify_password

SECRET_KEY = "3a9997e0def85136a115abcfd7575ec5be9b3726612b952436b728881a915d1f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

async def login(username: str, password: str, db: Session):
  """
  Authenticates a user and generates an access token.

  Attributes:
    username (str): The username of the user.
    password (str): The password of the user.
    db (Session): The database session.

  Returns:
    dict: A dictionary containing the access token and token type.

  Raises:
    HTTPException: If the username or password is incorrect.
  """

  user = authenticate_user(username, password, db=db)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )

  access_token_expires = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(data={"sub": user.email, "id": user.id}, expires_delta=access_token_expires)
  return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(username: str, password: str, db: Session):
  """
  Authenticates a user.

  Attributes:
    username (str): The username of the user.
    password (str): The password of the user.
    db (Session): The database session.

  Returns:
    Union[User, bool]: The authenticated user if successful, False otherwise.
  """
  user = db.query(User).filter(User.email == username).first()
  if not user:
    return False
  if not verify_password(password, user.password):
    return False
  return user

def create_access_token(data: dict, expires_delta: timedelta = None):
  """
  Creates an access token.

  Attributes:
    data (dict): The data to be encoded in the token.
    expires_delta (timedelta, optional): The expiration time delta. Defaults to None.

  Returns:
    str: The encoded access token.
  """
  to_encode = data.copy()
  # if expires_delta:
  #   expire = datetime.now() + expires_delta
  # else:
  #   expire = datetime.now() + timedelta(minutes=15)
  # to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
  """
  Retrieves the current user based on the access token.

  Attributes:
    token (str): The access token.

  Returns:
    dict: A dictionary containing the username and user ID of the current user.

  Raises:
    HTTPException: If the user cannot be validated.
  """
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get('sub')
    user_id: int = payload.get('id')
    if username is None or user_id is None:
      raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate user')
    return {'usename': username, 'id': user_id}

  except JWTError:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED,
              detail='Could not validate user')

user_dependency = Annotated[dict, Depends(get_current_user)]