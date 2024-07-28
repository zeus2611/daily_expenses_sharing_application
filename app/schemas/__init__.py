"""
app/schemas/__init__.py
This module contains the schema definitions for the daily expenses sharing application.

- UserBase: Base schema for user data.
- UserCreate: Schema for creating a new user.
- User: Schema for user data.

- ParticipantBase: Base schema for participant data.
- ParticipantCreate: Schema for creating a new participant.
- Participant: Schema for participant data.

- ExpenseBase: Base schema for expense data.
- ExpenseCreate: Schema for creating a new expense.
- Expense: Schema for expense data.
"""

from .user import UserBase, UserCreate, User
from .participant import ParticipantBase, ParticipantCreate, Participant
from .expense import ExpenseBase, ExpenseCreate, Expense
