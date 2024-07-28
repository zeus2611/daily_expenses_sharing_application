from fastapi import FastAPI
from .database import engine
from .models import Base
from app.routes import users, expenses

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Expense Tracker API",
        "status": "ok",
        "ping": "pong",
        "version": "1.0.0",
        "author": "Nischay",
        "Swagger UI": "http://localhost:8000/docs",
        "Redoc": "http://localhost:8000/redoc"
        }

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
