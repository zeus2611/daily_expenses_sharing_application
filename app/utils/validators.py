"""
app/utils/validators.py
The validators module for the Expense Tracker API.
"""

from app.schemas import ExpenseCreate

class ExpenseValidationError(Exception):
    """
    Custom exception class for expense

    Attributes:
        name (str): The name of the exception.
        message (str): The message of the exception.
    """
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message

def total_percentage(expense: ExpenseCreate):
    """
    Check if the total percentage of participants in the expense is equal to 100%.

    Args:
        expense (ExpenseCreate): The expense object containing participant details.

    Returns:
        bool: True if the total percentage is equal to 100, False otherwise.
    """
    return sum([p.percentage for p in expense.participants]) == 100

def total_amount(expense: ExpenseCreate):
    """
    Check if the total amount contributed by participants in the expense is equal to the total amount.

    Args:
        expense (ExpenseCreate): The expense object containing participant details.

    Returns:
        bool: True if the total amount is equal to the sum of participant amounts, False otherwise.
    """
    return sum([p.amount for p in expense.participants]) == expense.total_amount