from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import StreamingResponse
import pandas as pd
import io
from .. import operations, models, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    try:
        return operations.create_expense(db, expense)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{expense_id}", response_model=schemas.Expense)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = operations.get_expense(db, expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@router.get("/user/{user_id}", response_model=List[schemas.Participant])
def get_user_expenses(user_id: int, db: Session = Depends(get_db)):
    return operations.get_user_expenses(db, user_id)

@router.get("/balance-sheet/")
def download_balance_sheet(db: Session = Depends(get_db)):
    # Query for all expenses and users
    expenses = db.query(models.Expense).all()
    users = db.query(models.User).all()

    # Prepare the data
    data = []
    for expense in expenses:
        creator = db.query(models.User).filter_by(id=expense.creator_id).first()
        for participant in expense.participants:
            user = db.query(models.User).filter_by(id=participant.user_id).first()
            data.append({
                "Expense Description": expense.description,
                "Expense Amount": expense.total_amount,
                "Creator Name": creator.name if creator else "Unknown",
                "Participant Name": user.name if user else "Unknown",
                "Participant Amount Owed": participant.amount
            })

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=balance_sheet.csv"})
