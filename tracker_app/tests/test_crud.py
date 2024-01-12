import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate
from tracker_app.models import Project, Item
from tracker_app.serializers import ProjectSerializer, ItemSerializer

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_project():
    return Project.objects.create(name='Test Project', description='Project Description')

@pytest.fixture
def create_item():
    return Item.objects.create(name='Test Item')
    

@pytest.fixture
def test_user():
    return User.objects.create_user(username='testuser', email='test@user.com', password='test5595')
    

@pytest.mark.django_db
def test_project_list(api_client, test_user, create_project):
    force_authenticate(api_client, user=test_user)
    create_project('Test Project', 'Project Description')
    url = reverse('projects-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Project'

@pytest.mark.django_db
def test_project_create(api_client, test_user):
    force_authenticate(api_client, user=test_user)
    url = reverse('project-list')
    data = {
        'name': 'Test Project',
        'description': 'Project Description'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Project.objects.count() == 1
    assert Project.objects.last().name == 'Test Project'

@pytest.mark.django_db
def test_item_list(api_client, create_user, create_project, create_item):
    force_authenticate(api_client, user=test_user)
    project = create_project('Test Project', 'Project Description')
    item = create_item(project, 'Test Item')
    url = reverse('item-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Item'

@pytest.mark.django_db
def test_item_create(api_client, create_user, create_project):
    user = create_user('testuser', 'testpassword')
    api_client.login(username='testuser', password='testpassword')
    project = create_project(user, 'Test Project')
    url = reverse('item-list')
    data = {
        'project': project.id,
        'name': 'New Item'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Item.objects.count() == 2
    assert Item.objects.last().name == 'New Item'
