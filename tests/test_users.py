"""
tests/test_users.py
This file contains tests for the users endpoints.
The tests are as follows:
1. test_create_user: Tests the creation of a user.
2. test_create_user_with_duplicate_email: Tests the creation of a user with a duplicate email.
3. test_get_user_by_email: Tests the retrieval of a user by email.
4. test_get_user_with_invalid_email: Tests the retrieval of a user with an invalid email.
"""

def test_create_user(client):
    """
    Test case for creating a user.

    Args:
        client: The test client for making HTTP requests.

    Returns:
        None

    Raises:
        AssertionError: If the response status code is not 200 
        or if the response data does not match the expected values.
    """
    response = client.post("/users/", json={
        "email": "test@user.com",
        "name": "Test User",
        "mobile_number": "1234567890",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@user.com"
    assert data["name"] == "Test User"
    assert data["mobile_number"] == "1234567890"

def test_create_user_with_duplicate_email(client):
    """
    Test case to verify that creating a user with a duplicate email returns the expected response.

    Args:
        client: The test client for making HTTP requests.

    Returns:
        None

    Raises:
        AssertionError: If the response status code or 
        the error detail does not match the expected values.
    """
    response = client.post("/users/", json={
        "email": "duplicateuser@example.com",
        "name": "Duplicate User",
        "mobile_number": "0987654321",
        "password": "duplicatepassword"
    })
    assert response.status_code == 200

    response = client.post("/users/", json={
        "email": "duplicateuser@example.com",
        "name": "Duplicate User",
        "mobile_number": "0987654321",
        "password": "duplicatepassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_get_user_by_email(client):
    """
    Test case to verify the functionality of getting a user by email.

    Args:
        client (TestClient): The test client for making HTTP requests.

    Returns:
        None
    """
    # First, create a user
    client.post("/users/", json={
        "email": "getuser@example.com",
        "name": "Get User",
        "mobile_number": "1112223333",
        "password": "getuserpassword"
    })

    response = client.post("/auth/token", data={
        "username": "test@user.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/getuser@example.com", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "getuser@example.com"
    assert data["name"] == "Get User"
    assert data["mobile_number"] == "1112223333"

def test_get_user_with_invalid_email(client):
    """
    Test case to verify the behavior when trying to get a user with an invalid email.

    Args:
        client: The test client for making HTTP requests.

    Returns:
        None

    Raises:
        AssertionError: If the response status code or the 
        response detail does not match the expected values.
    """
    response = client.post("/auth/token", data={
        "username": "test@user.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/nonexistentuser@example.com", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
