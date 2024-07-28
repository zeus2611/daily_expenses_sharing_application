from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class SplitTypeEnum(enum.Enum):
    EQUAL = "EQUAL"
    EXACT = "EXACT"
    PERCENTAGE = "PERCENTAGE"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    mobile_number = Column(Integer, index=True)

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    total_amount = Column(Float, index=True)
    date = Column(Date, index=True)
    split_type = Column(Enum(SplitTypeEnum), index=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User")
    participants = relationship("Participant", back_populates="expense")

class Participant(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey('expenses.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    percentage = Column(Float)
    expense = relationship("Expense", back_populates="participants")
