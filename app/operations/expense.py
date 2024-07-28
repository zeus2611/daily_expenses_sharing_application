from sqlalchemy.orm import Session
from app import models
from app.schemas import ExpenseCreate
from app.utils.split_type import SplitTypeEnum
from app.operations.split import split_equal, split_exact, split_percentage

def create_expense(db: Session, expense: ExpenseCreate):
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
    
    if expense.split_type == SplitTypeEnum.EQUAL:
        split_equal(db, db_expense, expense)
    elif expense.split_type == SplitTypeEnum.EXACT:
        split_exact(db, db_expense, expense)
    elif expense.split_type == SplitTypeEnum.PERCENTAGE:
        split_percentage(db, db_expense, expense)
    
    db.commit()
    return db_expense

def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()

def get_user_expenses(db: Session, user_id: int):
    return db.query(models.Participant).filter(models.Participant.user_id == user_id).all()
