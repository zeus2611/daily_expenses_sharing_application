"""
app/main.py
The main module of the Expense Tracker API.
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .database import engine
from .models import Base
from app.routes import users, expenses

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    """
    Exception handler for ValueError.

    Args:
        request: The request object.
        exc (ValueError): The raised ValueError.

    Returns:
        JSONResponse: The JSON response with the error message.
    """
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

@app.get("/")
def read_root():
    """
    Root endpoint of the Expense Tracker API.

    Returns:
        dict: The response message with API information.
    """
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
