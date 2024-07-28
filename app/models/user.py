"""
app/models/user.py
User model module.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    """
    User model. 
    Represents a user in the database.

    Attributes:
        id (int): The ID of the user.
        email (str): The email of the user.
        name (str): The name of the user.
        mobile_number (str): The mobile number of the user.
        expenses (List[Expense]): The list of expenses created by the user.
        participants (List[Participant]): The list of expenses the user has participated in.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    mobile_number = Column(String, index=True)
    password = Column(String)
    expenses = relationship("Expense", back_populates="creator")
    participants = relationship("Participant", back_populates="user")
