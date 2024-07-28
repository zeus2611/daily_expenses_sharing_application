from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.token import Token
from app.utils.password import verify_password

router = APIRouter()

SECRET_KEY = "3a9997e0def85136a115abcfd7575ec5be9b3726612b952436b728881a915d1f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  print(form_data.username + " " + form_data.password)
  user = authenticate_user(form_data.username, form_data.password, db=db)
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
  user = db.query(User).filter(User.email == username).first()
  if not user:
    return False
  if not verify_password(password, user.password):
    return False
  return user

def create_access_token(data: dict, expires_delta: timedelta = None):
  to_encode = data.copy()
  # if expires_delta:
  #   expire = datetime.now() + expires_delta
  # else:
  #   expire = datetime.now() + timedelta(minutes=15)
  # to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
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

@router.get("/current_user", status_code=status.HTTP_200_OK)
async def user(user: user_dependency):
  if user is None:
    return HTTPException(status_code=401, detail="Authnetication failed")
  return {"user": user}