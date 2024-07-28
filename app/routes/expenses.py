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
from app.operations.auth import user_dependency

router = APIRouter()

def get_db():
    """
    Function to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Expense)
def create_expense(user: user_dependency, expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    """
    Route to create an expense.

    Attributes:
        user (dict): The user details.
        expense (ExpenseCreate): The expense details.
        db (Session): The database session.

    Returns:
        Expense: The created expense.
    """
    try:
        return operations.create_expense(user, db, expense)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/{expense_id}", response_model=schemas.Expense)
def get_expense(user: user_dependency, expense_id: int, db: Session = Depends(get_db)):
    """
    Route to get an expense by ID.

    Attributes:
        user (dict): The user details.
        expense_id (int): The expense ID.
        db (Session): The database session.

    Returns:
        Expense: The expense details.
    """
    db_expense = operations.get_expense(user, db, expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@router.get("/user/", response_model=List[schemas.Participant])
def get_user_expenses(user: user_dependency, db: Session = Depends(get_db)):
    """
    Route to get all expenses for a user.

    Attributes:
        user (dict): The user details.
        db (Session): The database session.

    Returns:
        List[Participant]: The list of expenses for the user.
    """
    return operations.get_user_expenses(user, db)

@router.get("/balance-sheet/")
def download_balance_sheet(db: Session = Depends(get_db)):
    """
    Route to download a balance sheet.

    Attributes:
        db (Session): The database session.

    Returns:
        StreamingResponse: The balance sheet CSV file.
    """
    data = operations.get_balance_sheet_data(db)
    csv_output = operations.generate_balance_sheet_csv(data)
    return StreamingResponse(csv_output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=balance_sheet.csv"})