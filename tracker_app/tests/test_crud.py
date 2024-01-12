import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate
from tracker_app.models import Project, Item, Store, QuoteRequest
from tracker_app.serializers import ProjectSerializer, ItemSerializer

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return User.objects.create_user(username='testuser', email='test@user.com', password='test5595')

@pytest.fixture
def test_project():
    return Project.objects.create(user=test_user, name='Test Project', description='Project Description')

@pytest.fixture
def test_item():
    return Item.objects.create(project=test_project, name='Test Item', description='Item Description')

@pytest.fixture
def test_store():
    return Store.objects.create(user=test_user, name='Test Store')

@pytest.fixture
def test_quoterequest():
    return QuoteRequest.objects.create(item=test_item, details='Quote Request Details', store=test_store)
        

@pytest.mark.django_db
def test_project_list(api_client, test_user, create_project):
    force_authenticate(api_client, user=test_user)
    url = reverse('projects-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Project'

@pytest.mark.django_db
def test_project_create(api_client, test_user):
    force_authenticate(api_client, user=test_user)
    url = reverse('projects-list')
    data = {
        'name': 'New Project',
        'description': 'Project Description'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Project.objects.count() == 2
    assert Project.objects.last().name == 'New Project'

@pytest.mark.django_db
def test_item_list(api_client):
    force_authenticate(api_client, user=test_user)
    url = reverse('items-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Item'

@pytest.mark.django_db
def test_item_create(api_client, test_user, test_project):
    force_authenticate(api_client, user=test_user)
    url = reverse('items-list')
    data = {
        'project': test_project.id,
        'name': 'New Item',
        'description': 'Item Description'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Item.objects.count() == 2
    assert Item.objects.last().name == 'New Item'

@pytest.mark.django_db
def test_store_list(api_client, test_user):
    force_authenticate(api_client, user=test_user)
    url = reverse('stores-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Store'

@pytest.mark.django_db
def test_store_create(api_client, test_user):
    force_authenticate(api_client, user=test_user)
    url = reverse('stores-list')
    data = {
        'name': 'New Store'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Store.objects.count() == 2
    assert Store.objects.last().name == 'New Store'

@pytest.mark.django_db
def test_quoterequest_list(api_client, test_user):
    force_authenticate(api_client, user=test_user)
    url = reverse('quoterequests-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['details'] == 'Quote Request Details'

@pytest.mark.django_db
def test_quoterequest_create(api_client, test_user, test_item, test_store):
    force_authenticate(api_client, user=test_user)
    url = reverse('quoterequests-list')
    data = {
        'item': test_item.id,
        'details': 'New Quote Request',
        'store': test_store.id
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert QuoteRequest.objects.count() == 2
    assert QuoteRequest.objects.last().details == 'New Quote Request'
