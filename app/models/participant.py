from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Participant(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey('expenses.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    percentage = Column(Float)
    expense = relationship("Expense", back_populates="participants")
    user = relationship("User", back_populates="participants")
