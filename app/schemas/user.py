from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    name: str
    mobile_number: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
