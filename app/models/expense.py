"""
app/models/expense.py
Expense model module.
"""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.split_type import SplitTypeEnum
from .participant import Participant

class Expense(Base):
    """
    Expense model class.
    Represents an expense in the database.

    Attributes:
        id (int): The ID of the expense.
        description (str): The description of the expense.
        total_amount (float): The total amount of the expense.
        date (Date): The date of the expense.
        split_type (SplitTypeEnum): The type of split for the expense.
        creator_id (int): The ID of the creator of the expense.
        creator (User): The creator of the expense.
        participants (List[Participant]): The list of participants in the expense.
    """

    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    total_amount = Column(Float, index=True)
    date = Column(Date, index=True)
    split_type = Column(Enum(SplitTypeEnum), index=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="expenses")
    participants = relationship("Participant", back_populates="expense")
