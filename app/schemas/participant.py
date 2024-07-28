"""
app/schemas/participant.py
This module contains the Pydantic models for the participant in an expense.
It includes the ParticipantBase, ParticipantCreate, and Participant models.
"""

from pydantic import BaseModel
from typing import Optional

class ParticipantBase(BaseModel):
    """
    Base model for a participant in an expense.

    Attributes:
        user_id (int): The ID of the user participating in the expense.
        amount (Optional[float]): The amount the user owes for the expense.
        percentage (Optional[float]): The percentage the user owes for the expense.
    """

    user_id: int
    amount: Optional[float] = None
    percentage: Optional[float] = None

class ParticipantCreate(ParticipantBase):
    """
    Model for creating a new participant in an expense.
    Inherits from ParticipantBase.
    """

    pass

class Participant(ParticipantBase):
    """
    Model for a participant in an expense.
    Inherits from ParticipantBase.

    Attributes:
        id (int): The ID of the participant.
        expense_id (int): The ID of the expense the participant is associated with.
    """

    id: int
    expense_id: int

    class Config:
        """
        Configuration class for the Participant model.
        """

        orm_mode = True
