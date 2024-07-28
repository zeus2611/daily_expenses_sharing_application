"""
app/operations/split.py
This module contains the functions to split an expense 
amount among participants based on the split type.
The split types include EQUAL, EXACT, and PERCENTAGE.
For Exact: The total amount distributed among participants 
must equal the total expense amount
For Percentage: The total percentage of participants must be 100%.
"""

from sqlalchemy.orm import Session
from app.models import Participant, Expense
from app.schemas import ExpenseCreate
from app.utils.validators import total_percentage, total_amount, ExpenseValidationError

def split_equal(db: Session, db_expense: Expense, expense: ExpenseCreate):
    """
    Split the expense amount equally among all participants.

    Attributes:
        db (Session): The database session.
        db_expense (Expense): The created expense in the database.
        expense (ExpenseCreate): The expense

    Returns:
        None
    """
    amount_per_person = expense.total_amount / len(expense.participants)
    for participant in expense.participants:
        db_participant = Participant(expense_id=db_expense.id, user_id=participant.user_id, amount=amount_per_person)
        db.add(db_participant)

def split_exact(db: Session, db_expense: Expense, expense: ExpenseCreate):
    """
    Split the expense amount exactly as specified by the user.

    Attributes:
        db (Session): The database session.
        db_expense (Expense): The created expense in the database.
        expense (ExpenseCreate): The expense
    
    Returns:
        None
    """
    if not total_amount(expense):
        msg="The total amount distributed among participants must equal the total expense amount"
        raise ExpenseValidationError(
            name="TotalAmountError",
            message=msg)
    for participant in expense.participants:
        db_participant = Participant(expense_id=db_expense.id, user_id=participant.user_id, amount=participant.amount)
        db.add(db_participant)

def split_percentage(db: Session, db_expense: Expense, expense: ExpenseCreate):
    """
    Split the expense amount based on the percentage specified by the user.

    Attributes:
        db (Session): The database session.
        db_expense (Expense): The created expense in the database.
        expense (ExpenseCreate): The expense

    Returns:
        None
    """
    if not total_percentage(expense):
        msg="The total percentage of participants must be 100%"
        raise ExpenseValidationError(name="TotalPercentageError", message=msg)
    for participant in expense.participants:
        amount = expense.total_amount * (participant.percentage / 100)
        db_participant = Participant(expense_id=db_expense.id, user_id=participant.user_id, amount=amount, percentage=participant.percentage)
        db.add(db_participant)
