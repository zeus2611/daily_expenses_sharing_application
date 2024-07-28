from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, name=user.name, mobile_number=user.mobile_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_expense(db: Session, expense: schemas.ExpenseCreate):
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
    
    if expense.split_type == schemas.SplitTypeEnum.EQUAL:
        amount_per_person = expense.total_amount / len(expense.participants)
        for participant in expense.participants:
            db_participant = models.Participant(expense_id=db_expense.id, user_id=participant.user_id, amount=amount_per_person)
            db.add(db_participant)
    
    elif expense.split_type == schemas.SplitTypeEnum.EXACT:
        for participant in expense.participants:
            db_participant = models.Participant(expense_id=db_expense.id, user_id=participant.user_id, amount=participant.amount)
            db.add(db_participant)
    
    elif expense.split_type == schemas.SplitTypeEnum.PERCENTAGE:
        total_percentage = sum([p.percentage for p in expense.participants])
        if total_percentage != 100:
            raise ValueError("Total percentage must equal 100")
        for participant in expense.participants:
            amount = expense.total_amount * (participant.percentage / 100)
            db_participant = models.Participant(expense_id=db_expense.id, user_id=participant.user_id, amount=amount, percentage=participant.percentage)
            db.add(db_participant)
    
    db.commit()
    return db_expense

def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()

def get_user_expenses(db: Session, user_id: int):
    return db.query(models.Participant).filter(models.Participant.user_id == user_id).all()
