from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.split_type import SplitTypeEnum
from .participant import Participant

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    total_amount = Column(Float, index=True)
    date = Column(Date, index=True)
    split_type = Column(Enum(SplitTypeEnum), index=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="expenses")
    participants = relationship("Participant", back_populates="expense")
