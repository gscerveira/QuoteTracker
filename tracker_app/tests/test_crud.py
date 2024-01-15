import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tracker_app.models import Item, Project, QuoteRequest, Store

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="testuser", email="test@user.com", password="test5595"
    )


@pytest.fixture
def test_user2():
    return User.objects.create_user(
        username="testuser2", email="test@user2.com", password="test5595"
    )


@pytest.fixture
def test_project(test_user):
    return Project.objects.create(
        user=test_user, name="Test Project", description="Project Description"
    )


@pytest.fixture
def test_item(test_project):
    return Item.objects.create(
        project=test_project, name="Test Item", description="Item Description"
    )


@pytest.fixture
def test_store(test_user):
    return Store.objects.create(user=test_user, name="Test Store")


@pytest.fixture
def test_quoterequest(test_item, test_store):
    return QuoteRequest.objects.create(
        item=test_item, details="Quote Request Details", store=test_store
    )


# Project Tests


# Read
@pytest.mark.django_db
def test_project_list(api_client, test_user, test_project):
    api_client.force_authenticate(user=test_user)
    url = reverse("projects-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Test Project"


# Create
@pytest.mark.django_db
def test_project_create(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    url = reverse("projects-list")
    data = {"name": "New Project", "description": "Project Description"}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Project.objects.count() == 1
    assert Project.objects.last().name == "New Project"


# Update
@pytest.mark.django_db
def test_project_update(api_client, test_user, test_project):
    api_client.force_authenticate(user=test_user)
    url = reverse("projects-detail", args=[test_project.id])
    data = {"name": "Updated Project", "description": "Updated Project Description"}
    response = api_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert Project.objects.count() == 1
    assert Project.objects.last().name == "Updated Project"
    assert Project.objects.last().description == "Updated Project Description"


# Unauthorized Update
@pytest.mark.django_db
def test_project_unauthorized_update(api_client, test_user2, test_project):
    api_client.force_authenticate(user=test_user2)
    url = reverse("projects-detail", args=[test_project.id])
    data = {"name": "Updated Project", "description": "Updated Project Description"}
    response = api_client.patch(url, data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Project.objects.count() == 1
    assert Project.objects.last().name == "Test Project"
    assert Project.objects.last().description == "Project Description"


# Delete
@pytest.mark.django_db
def test_project_delete(api_client, test_user, test_project):
    api_client.force_authenticate(user=test_user)
    url = reverse("projects-detail", args=[test_project.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Project.objects.count() == 0
    assert Item.objects.count() == 0
    assert QuoteRequest.objects.count() == 0


# Unauthorized Delete
@pytest.mark.django_db
def test_project_unauthorized_delete(api_client, test_user2, test_project):
    api_client.force_authenticate(user=test_user2)
    url = reverse("projects-detail", args=[test_project.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Project.objects.count() == 1


# Item Tests


# Read
@pytest.mark.django_db
def test_item_list(api_client, test_user, test_item):
    api_client.force_authenticate(user=test_user)
    url = reverse("items-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Test Item"


# Create
@pytest.mark.django_db
def test_item_create(api_client, test_user, test_project):
    api_client.force_authenticate(user=test_user)
    url = reverse("items-list")
    data = {
        "project": test_project.id,
        "name": "New Item",
        "description": "Item Description",
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Item.objects.count() == 1
    assert Item.objects.last().name == "New Item"


# Update
@pytest.mark.django_db
def test_item_update(api_client, test_user, test_item):
    api_client.force_authenticate(user=test_user)
    url = reverse("items-detail", args=[test_item.id])
    data = {"name": "Updated Item", "description": "Updated Item Description"}
    response = api_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert Item.objects.count() == 1
    assert Item.objects.last().name == "Updated Item"
    assert Item.objects.last().description == "Updated Item Description"


# Unauthorized Update
@pytest.mark.django_db
def test_item_unauthorized_update(api_client, test_user2, test_item):
    api_client.force_authenticate(user=test_user2)
    url = reverse("items-detail", args=[test_item.id])
    data = {"name": "Updated Item", "description": "Updated Item Description"}
    response = api_client.patch(url, data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Item.objects.count() == 1
    assert Item.objects.last().name == "Test Item"
    assert Item.objects.last().description == "Item Description"


# Delete
@pytest.mark.django_db
def test_item_delete(api_client, test_user, test_item):
    api_client.force_authenticate(user=test_user)
    url = reverse("items-detail", args=[test_item.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Item.objects.count() == 0
    assert QuoteRequest.objects.count() == 0


# Unauthorized Delete
@pytest.mark.django_db
def test_item_unauthorized_delete(api_client, test_user2, test_item):
    api_client.force_authenticate(user=test_user2)
    url = reverse("items-detail", args=[test_item.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Item.objects.count() == 1


# Store Tests
# Read
@pytest.mark.django_db
def test_store_list(api_client, test_user, test_store):
    api_client.force_authenticate(user=test_user)
    url = reverse("stores-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Test Store"


# Create
@pytest.mark.django_db
def test_store_create(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    url = reverse("stores-list")
    data = {"name": "New Store"}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Store.objects.count() == 1
    assert Store.objects.last().name == "New Store"


# Update
@pytest.mark.django_db
def test_store_update(api_client, test_user, test_store):
    api_client.force_authenticate(user=test_user)
    url = reverse("stores-detail", args=[test_store.id])
    data = {"name": "Updated Store"}
    response = api_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert Store.objects.count() == 1
    assert Store.objects.last().name == "Updated Store"


# Unauthorized Update
@pytest.mark.django_db
def test_store_unauthorized_update(api_client, test_user2, test_store):
    api_client.force_authenticate(user=test_user2)
    url = reverse("stores-detail", args=[test_store.id])
    data = {"name": "Updated Store"}
    response = api_client.patch(url, data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Store.objects.count() == 1
    assert Store.objects.last().name == "Test Store"


# Delete
@pytest.mark.django_db
def test_store_delete(api_client, test_user, test_store):
    api_client.force_authenticate(user=test_user)
    url = reverse("stores-detail", args=[test_store.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Store.objects.count() == 0


# Unauthorized Delete
@pytest.mark.django_db
def test_store_unauthorized_delete(api_client, test_user2, test_store):
    api_client.force_authenticate(user=test_user2)
    url = reverse("stores-detail", args=[test_store.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Store.objects.count() == 1


# QuoteRequest Tests
# Read
@pytest.mark.django_db
def test_quoterequest_list(api_client, test_user, test_quoterequest):
    api_client.force_authenticate(user=test_user)
    url = reverse("quoterequests-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["details"] == "Quote Request Details"


# Create
@pytest.mark.django_db
def test_quoterequest_create(api_client, test_user, test_item, test_store):
    api_client.force_authenticate(user=test_user)
    url = reverse("quoterequests-list")
    data = {
        "item": test_item.id,
        "details": "New Quote Request",
        "store": test_store.id,
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert QuoteRequest.objects.count() == 1
    assert QuoteRequest.objects.last().details == "New Quote Request"


# Update
@pytest.mark.django_db
def test_quoterequest_update(api_client, test_user, test_quoterequest):
    api_client.force_authenticate(user=test_user)
    url = reverse("quoterequests-detail", args=[test_quoterequest.id])
    data = {"details": "Updated Quote Request"}
    response = api_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert QuoteRequest.objects.count() == 1
    assert QuoteRequest.objects.last().details == "Updated Quote Request"


# Unauthorized Update
@pytest.mark.django_db
def test_quoterequest_unauthorized_update(api_client, test_user2, test_quoterequest):
    api_client.force_authenticate(user=test_user2)
    url = reverse("quoterequests-detail", args=[test_quoterequest.id])
    data = {"details": "Updated Quote Request"}
    response = api_client.patch(url, data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert QuoteRequest.objects.count() == 1
    assert QuoteRequest.objects.last().details == "Quote Request Details"


# Delete
@pytest.mark.django_db
def test_quoterequest_delete(api_client, test_user, test_quoterequest):
    api_client.force_authenticate(user=test_user)
    url = reverse("quoterequests-detail", args=[test_quoterequest.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert QuoteRequest.objects.count() == 0


# Unauthorized Delete
@pytest.mark.django_db
def test_quoterequest_unauthorized_delete(api_client, test_user2, test_quoterequest):
    api_client.force_authenticate(user=test_user2)
    url = reverse("quoterequests-detail", args=[test_quoterequest.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert QuoteRequest.objects.count() == 1
