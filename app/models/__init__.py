"""
app/models/__init__.py
This file is used to import all the models in the app.
This allows us to import all the models in a single line in other files.
For example, instead of importing each model separately in 
app/operations/expense.py: from app.models.expense import Expense
we can import all the models in a single line:
from app.models import Expense
"""

from app.database import Base

from .user import User
from .expense import Expense
from .participant import Participant
