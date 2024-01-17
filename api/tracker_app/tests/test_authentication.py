import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_register_user(api_client):
    """
    Test case to register a new user.

    It sends a POST request to the 'register' endpoint with user data.
    It asserts that the response status code is 201 (Created) and
    checks if the user is successfully created in the database.
    """
    url = reverse("register")
    user_data = {
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "pass5595",
    }
    response = api_client.post(url, user_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.get().username == "testuser"

@pytest.mark.django_db
def test_login_user(api_client):
    """
    Test case to login a user.

    It creates a user in the database using User.objects.create_user().
    It sends a POST request to the 'login' endpoint with correct credentials
    and asserts that the response status code is 200 (OK).
    It then sends a POST request with incorrect credentials and asserts
    that the response status code is 401 (Unauthorized).
    """
    User.objects.create_user(
        username="testuser", email="testuser@test.com", password="pass5595"
    )

    # Correct credentials
    url = reverse("login")
    user_data = {"username": "testuser", "password": "pass5595"}
    response = api_client.post(url, user_data, format="json")
    assert response.status_code == status.HTTP_200_OK

    # Incorrect credentials
    user_data = {"username": "testuser", "password": "wrong5595"}
    response = api_client.post(url, user_data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_logout_user(api_client):
    """
    Test case to logout a user.

    It creates a user in the database using User.objects.create_user().
    It logs in the user using api_client.login().
    It sends a POST request to the 'logout' endpoint and asserts that
    the response status code is 204 (No Content).
    It then tries to access a protected URL and asserts that the response
    status code is 403 (Forbidden).
    """
    user = User.objects.create_user(
        username="testuser", email="testuser@test.com", password="pass5595"
    )
    api_client.login(username="testuser", password="pass5595")

    # Logout
    url = reverse("logout")
    response = api_client.post(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Try to access protected url
    url_projects = reverse("projects-list")
    response = api_client.get(url_projects)
    assert response.status_code == status.HTTP_403_FORBIDDEN
