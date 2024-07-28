"""
app/routes/expenses.py
This module contains the routes for the expenses API.
It includes routes to create an expense, get an expense by ID,
get all expenses for a user, and download a balance sheet.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from .. import operations, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    """
    Create a new database session for each request.

    Returns:
        Session: The database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    """
    Create an expense in the database.

    Attributes:
        expense (ExpenseCreate): The expense details.
        db (Session): The database session.

    Returns:
        Expense: The created expense.
    """
    try:
        return operations.create_expense(db, expense)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/{expense_id}", response_model=schemas.Expense)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    """
    Get an expense by ID.

    Attributes:
        expense_id (int): The ID of the expense.
        db (Session): The database session.

    Returns:
        Expense: The expense with the specified ID.
    """
    db_expense = operations.get_expense(db, expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@router.get("/user/{user_id}", response_model=List[schemas.Participant])
def get_user_expenses(user_id: int, db: Session = Depends(get_db)):
    """
    Get all expenses for a user.

    Attributes:
        user_id (int): The ID of the user.
        db (Session): The database session.

    Returns:
        List[Participant]: The list of expenses for the user.
    """
    return operations.get_user_expenses(db, user_id)

@router.get("/balance-sheet/")
def download_balance_sheet(db: Session = Depends(get_db)):
    """
    Download the Expense balance sheet CSV file.

    Attributes:
        db (Session): The database session.

    Returns:
        StreamingResponse: The balance sheet CSV file.
    """
    data = operations.get_balance_sheet_data(db)
    csv_output = operations.generate_balance_sheet_csv(data)
    return StreamingResponse(csv_output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=balance_sheet.csv"})