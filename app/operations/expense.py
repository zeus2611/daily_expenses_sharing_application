"""
app/operations/expense.py
This module contains the operations related to expenses.
It includes functions to create an expense, get an expense 
by ID, get all expenses for a user, get balance sheet data, 
and generate a balance sheet CSV file.
"""

import io
from sqlalchemy.orm import Session
import pandas as pd
from app import models
from app.schemas import ExpenseCreate
from app.utils.split_type import SplitTypeEnum
from app.operations.split import split_equal, split_exact, split_percentage

def create_expense(db: Session, expense: ExpenseCreate):
    """
    Create an expense in the database.

    Attributes:
        db (Session): The database session.
        expense (ExpenseCreate): The expense details.

    Returns:
        Expense: The created expense.
    """
    db_expense = models.Expense(
        description=expense.description,
        total_amount=expense.total_amount,
        date=expense.date,
        split_type=expense.split_type,
        creator_id=expense.creator_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    # Split the expense amount among participants based on the split type.
    # For example, if the split type is EQUAL, the expense amount will be split equally among all participants.
    if expense.split_type == SplitTypeEnum.EQUAL:
        split_equal(db, db_expense, expense)

    # If the split type is EXACT, the expense amount will be split exactly as specified by the user.
    elif expense.split_type == SplitTypeEnum.EXACT:
        split_exact(db, db_expense, expense)

    # If the split type is PERCENTAGE, the expense amount will be split based on the percentage specified by the user.
    elif expense.split_type == SplitTypeEnum.PERCENTAGE:
        split_percentage(db, db_expense, expense)
    
    db.commit()
    return db_expense

def get_expense(db: Session, expense_id: int):
    """
    Get an expense by ID.
    An expense consists of the expense details, the creator of the expense, and the participants in the expense.

    Attributes:
        db (Session): The database session.
        expense_id (int): The ID of the expense.

    Returns:
        Expense: The expense with the specified ID.
    """
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()

def get_user_expenses(db: Session, user_id: int):
    """
    Get all expenses for a user.

    Attributes:
        db (Session): The database session.
        user_id (int): The ID of the user.
    
    Returns:
        List[Expense]: The list of expenses for the user.
    """
    return db.query(models.Participant).filter(models.Participant.user_id == user_id).all()

def get_balance_sheet_data(db: Session):
    """
    Get the balance sheet data.

    Attributes:
        db (Session): The database session.

    Returns:
        List[Dict]: The balance sheet data.
    """
    # Query for all expenses and users
    expenses = db.execute(db.query(models.Expense))
    expenses = expenses.scalars().all()
    users = db.execute(db.query(models.User))
    users = users.scalars().all()

    # Prepare the data
    data = []
    for expense in expenses:
        creator = db.execute(db.query(models.User).filter_by(id=expense.creator_id))
        creator = creator.scalar()
        participants = db.execute(db.query(models.Participant).filter_by(expense_id=expense.id))
        participants = participants.scalars().all()
        for participant in participants:
            user = db.execute(db.query(models.User).filter_by(id=participant.user_id))
            user = user.scalar()
            data.append({
                "Expense Description": expense.description,
                "Expense Amount": expense.total_amount,
                "Creator Name": creator.name if creator else "Unknown",
                "Participant Name": user.name if user else "Unknown",
                "Participant Amount Owed": participant.amount
            })
    return data

def generate_balance_sheet_csv(data):
    """
    Generate a balance sheet CSV file from the data.

    Attributes:
        data (List[Dict]): The balance sheet data.
    
    Returns:
        StringIO: The CSV file as a StringIO object.
    """
    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return output
