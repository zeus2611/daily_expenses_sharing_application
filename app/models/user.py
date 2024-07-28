from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    mobile_number = Column(Integer, index=True)
    expenses = relationship("Expense", back_populates="creator")
    participants = relationship("Participant", back_populates="user")
