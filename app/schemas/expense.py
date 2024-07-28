from pydantic import BaseModel
from typing import List
from datetime import date
from app.utils.split_type import SplitTypeEnum
from .user import User
from .participant import ParticipantCreate, Participant

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
