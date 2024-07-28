"""
app/schemas/expense.py
This module contains the Pydantic models for the Expense entity.
It includes the ExpenseBase, ExpenseCreate, and Expense models.
"""

from pydantic import BaseModel, Field
from typing import List
from datetime import date
from app.utils.split_type import SplitTypeEnum
from .user import User
from .participant import ParticipantCreate, Participant

class ExpenseBase(BaseModel):
    """
    Represents the base model for an expense.

    Attributes:
        description (str): The description of the expense.
        total_amount (float): The total amount of the expense.
        date (date): The date of the expense.
        split_type (SplitTypeEnum): The type of split for the expense.
        creator_id (int): The ID of the creator of the expense.
        participants (List[ParticipantCreate]): The list of participants in the expense.
    """
    description: str
    total_amount: float
    date: date
    split_type: SplitTypeEnum
    creator_id: int
    participants: List[ParticipantCreate]

class ExpenseCreate(ExpenseBase):
    """
    Represents the model for creating an expense.
    Inherits from ExpenseBase.

    No additional attributes.
    """
    pass

class Expense(ExpenseBase):
    """
    Represents the model for an expense.
    Inherits from ExpenseBase.

    Attributes:
        id (int): The ID of the expense.
        creator (User): The creator of the expense.
        participants (List[Participant]): The list of participants in the expense.
    """
    id: int
    creator: User
    participants: List[Participant] = Field(..., min_items=1)

    class Config:
        """
        Configuration class for the Expense model.
        """
        orm_mode = True
