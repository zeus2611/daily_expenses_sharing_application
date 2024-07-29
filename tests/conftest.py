"""
tests/conftest.py
This file contains fixtures that are used across multiple test files.
The fixtures are as follows:
1. client: A fixture that creates a test client for making HTTP requests.
2. get_db: A fixture that creates a new database session for each test.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

def get_db():
    """
    Returns a database session for testing purposes.

    Yields:
        db: A database session object.

    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        Base.metadata.drop_all(bind=engine)
        db.close()

app.dependency_overrides[get_db] = get_db

@pytest.fixture(scope="module")
def client():
    """
    Creates a test client for making HTTP requests.

    Yields:
        c: A test client object.

    """
    with TestClient(app) as c:
        yield c
