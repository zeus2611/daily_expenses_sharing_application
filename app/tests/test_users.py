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
    # models.Base.metadata.drop_all(bind=engine)
    db.close()

def test_create_user(test_db):
    response = client.post("/users/", json={
        "email": "testuser@example.com",
        "name": "Test User",
        "mobile_number": "1234567890"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["name"] == "Test User"
    assert data["mobile_number"] == "1234567890"

def test_get_user(test_db):
    # First, create a user
    response = client.post("/users/", json={
        "email": "testuser2@example.com",
        "name": "Test User 2",
        "mobile_number": "0987654321"
    })
    assert response.status_code == 200
    created_user = response.json()
    
    user_id = created_user["id"]

    # Now retrieve the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser2@example.com"
    assert data["name"] == "Test User 2"
    assert data["mobile_number"] == "0987654321"

def test_get_nonexistent_user(test_db):
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
