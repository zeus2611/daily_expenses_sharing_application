"""
tests/test_expenses.py
This file contains tests for the expenses endpoints.
The tests are as follows:
1. test_create_user: Tests the creation of a user.
2. test_create_expense: Tests the creation of an expense.
3. test_get_expense: Tests the retrieval of an expense.
4. test_get_expense_other: Tests the retrieval of an expense that does not exist.
5. test_get_user_expenses: Tests the retrieval of all expenses for a user.
6. test_download_balance_sheet: Tests the download of a balance sheet.
"""

def test_create_user(client):
    """
    Test case for creating a user.

    Args:
        client (TestClient): The test client for making HTTP requests.

    Returns:
        None
    """
    response = client.post("/users/", json={
        "email": "testuser@example.com",
        "name": "Test User",
        "mobile_number": "1234567890",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

def test_create_expense(client):
    """
    Test case for creating an expense.

    Args:
        client (TestClient): The test client for making HTTP requests.

    Returns:
        None
    """
    response = client.post("/auth/token", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    expense_data = {
        "description": "Test Expense",
        "total_amount": 100,
        "date": "2024-07-01",
        "split_type": "EQUAL",
        "creator_id": 1,
        "participants": [{"user_id": 1}]
    }
    response = client.post("/expenses/", json=expense_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test Expense"
    assert data["total_amount"] == 100

def test_get_expense(client):
    """
    Test case for getting an expense.

    Args:
        client (TestClient): The test client for making HTTP requests.

    Returns:
        None
    """
    response = client.post("/auth/token", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/expenses/1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test Expense"
    assert data["total_amount"] == 100

def test_get_expense_other(client):
    """
    Test case for retrieving an expense that does not belong to the user.

    Args:
        client (TestClient): The test client for making HTTP requests.

    Returns:
        None
    """
    response = client.post("/auth/token", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/expenses/20", headers=headers)
    print(response.json())
    assert response.status_code == 400

def test_get_user_expenses(client):
    """
    Test case for retrieving expenses of a user.

    Args:
        client (TestClient): The test client for making HTTP requests.

    Returns:
        None
    """
    response = client.post("/auth/token", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/expenses/user/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["expense_id"] == 1

def test_download_balance_sheet(client):
    """
    Test case for downloading the balance sheet.

    Args:
        client (TestClient): The test client object.

    Returns:
        None
    """
    response = client.get("/expenses/balance-sheet/")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=balance_sheet.csv"
