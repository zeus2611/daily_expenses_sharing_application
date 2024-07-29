import bcrypt

def hash_password(password: str) -> str:
  salt = bcrypt.gensalt()
  return bcrypt.hashpw(password.encode(), salt=salt).decode()

def verify_password(password: str, hashed_password: str) -> bool:
  return bcrypt.checkpw(password.encode(), hashed_password.encode())
