from app.schemas import ExpenseCreate

def total_percentage(expense: ExpenseCreate):
    return sum([p.percentage for p in expense.participants]) == 100

def total_amount(expense: ExpenseCreate):
    return sum([p.amount for p in expense.participants]) == expense.total_amount