from sqlalchemy.orm import Session
from app import models
from app.schemas import ExpenseCreate
from app.utils.validators import total_percentage, total_amount

def split_equal(db: Session, db_expense: models.Expense, expense: ExpenseCreate):
    amount_per_person = expense.total_amount / len(expense.participants)
    for participant in expense.participants:
        db_participant = models.Participant(expense_id=db_expense.id, user_id=participant.user_id, amount=amount_per_person)
        db.add(db_participant)

def split_exact(db: Session, db_expense: models.Expense, expense: ExpenseCreate):
    if not total_amount(expense):
        raise ValueError("Total amount must be equal to sum of individual amounts")
    for participant in expense.participants:
        db_participant = models.Participant(expense_id=db_expense.id, user_id=participant.user_id, amount=participant.amount)
        db.add(db_participant)

def split_percentage(db: Session, db_expense: models.Expense, expense: ExpenseCreate):
    if not total_percentage(expense):
        raise ValueError("Total percentage must equal 100")
    for participant in expense.participants:
        amount = expense.total_amount * (participant.percentage / 100)
        db_participant = models.Participant(expense_id=db_expense.id, user_id=participant.user_id, amount=amount, percentage=participant.percentage)
        db.add(db_participant)
