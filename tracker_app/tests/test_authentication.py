import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your tests here.


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_user(api_client):
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
