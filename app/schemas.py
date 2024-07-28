from pydantic import BaseModel, Field, conlist, constr, conint
from typing import List, Optional
from datetime import date
from enum import Enum

class SplitTypeEnum(str, Enum):
    EQUAL = "EQUAL"
    EXACT = "EXACT"
    PERCENTAGE = "PERCENTAGE"

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

class ParticipantBase(BaseModel):
    user_id: int
    amount: Optional[float] = None
    percentage: Optional[float] = None

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    id: int
    expense_id: int

    class Config:
        orm_mode = True

class ExpenseBase(BaseModel):
    description: str
    total_amount: float
    date: date
    split_type: SplitTypeEnum
    creator_id: int
    participants: List[ParticipantCreate]

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    creator: User
    participants: List[Participant]

    class Config:
        orm_mode = True
