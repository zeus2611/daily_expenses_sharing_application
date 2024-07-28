from pydantic import BaseModel
from typing import Optional

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
