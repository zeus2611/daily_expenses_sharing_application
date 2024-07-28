import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine
from app import models

# Create a test client
client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    # Setup database
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    # Teardown database
    models.Base.metadata.drop_all(bind=engine)
    db.close()

def test_create_equal_expense(test_db):
    response = client.post("/expenses/", json={
        "description": "Dinner",
        "total_amount": 3000,
        "date": "2024-07-27",
        "split_type": "EQUAL",  # Ensure this matches the Enum
        "creator_id": 1,
        "participants": [
            {"user_id": 1},
            {"user_id": 2},
            {"user_id": 3}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Dinner"
    assert data["total_amount"] == 3000
    assert data["split_type"] == "EQUAL"
    assert data["creator_id"] == 1

def test_create_exact_expense(test_db):
    response = client.post("/expenses/", json={
        "description": "Shopping",
        "total_amount": 4299,
        "date": "2024-07-27",
        "split_type": "EXACT",  # Ensure this matches the Enum
        "creator_id": 1,
        "participants": [
            {"user_id": 1, "amount": 799},
            {"user_id": 2, "amount": 2000},
            {"user_id": 3, "amount": 1500}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Shopping"
    assert data["total_amount"] == 4299
    assert data["split_type"] == "EXACT"
    assert data["creator_id"] == 1

def test_create_percentage_expense(test_db):
    response = client.post("/expenses/", json={
        "description": "Party",
        "total_amount": 4000,
        "date": "2024-07-27",
        "split_type": "PERCENTAGE",  # Ensure this matches the Enum
        "creator_id": 1,
        "participants": [
            {"user_id": 1, "percentage": 50},
            {"user_id": 2, "percentage": 25},
            {"user_id": 3, "percentage": 25}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Party"
    assert data["total_amount"] == 4000
    assert data["split_type"] == "PERCENTAGE"
    assert data["creator_id"] == 1

# def test_create_invalid_percentage_expense(test_db):
#     response = client.post("/expenses/", json={
#         "description": "Party",
#         "total_amount": 4000,
#         "date": "2024-07-27",
#         "split_type": "PERCENTAGE",
#         "creator_id": 1,
#         "participants": [
#             {"user_id": 1, "percentage": 40},
#             {"user_id": 2, "percentage": 30},
#             {"user_id": 3, "percentage": 30}
#         ]
#     })
#     assert response.status_code == 400
#     data = response.json()
#     assert data["detail"] == "Total percentage must equal 100"

def test_get_expense(test_db):
    # First, create an expense
    response = client.post("/expenses/", json={
        "description": "Dinner",
        "total_amount": 3000,
        "date": "2024-07-27",
        "split_type": "EQUAL",  # Ensure this matches the Enum
        "creator_id": 1,
        "participants": [
            {"user_id": 1},
            {"user_id": 2},
            {"user_id": 3}
        ]
    })
    assert response.status_code == 200
    created_expense = response.json()
    
    expense_id = created_expense["id"]

    # Now retrieve the expense
    response = client.get(f"/expenses/{expense_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Dinner"
    assert data["total_amount"] == 3000
    assert data["split_type"] == "EQUAL"
    assert data["creator_id"] == 1

def test_get_nonexistent_expense(test_db):
    response = client.get("/expenses/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Expense not found"}
