"""
app/models/participant.py
Participant model module.
"""

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Participant(Base):
    """Participant model class.
    Represents a participant in the database.

    Attributes:
        id (int): The ID of the participant.
        expense_id (int): The ID of the expense the participant is associated with.
        user_id (int): The ID of the user participating in the expense.
        amount (float): The amount the user owes for the expense.
        percentage (float): The percentage the user owes for the expense.
        expense (Expense): The expense the participant is associated with.
        user (User): The user participating in the expense.
    """
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey('expenses.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    percentage = Column(Float)
    expense = relationship("Expense", back_populates="participants")
    user = relationship("User", back_populates="participants")
