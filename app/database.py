"""
app/database.py
This module provides the necessary tools for interacting with the database.

- `engine`: The SQLAlchemy engine object that connects to the SQLite database.
- `SessionLocal`: A session factory that creates new SQLAlchemy sessions.
- `Base`: The base class for SQLAlchemy models, allowing them to be defined declaratively.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./expenses.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
