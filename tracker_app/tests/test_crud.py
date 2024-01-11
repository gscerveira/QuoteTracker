import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from .models import Project, Item
from .serializers import ProjectSerializer, ItemSerializer

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_project():
    def _create_project(name, description):
        return Project.objects.create(name=name, description=description)
    return _create_project

@pytest.fixture
def create_item():
    def _create_item(project, name):
        return Item.objects.create(project=project, name=name)
    return _create_item

@pytest.fixture
def create_user():
    def _create_user(username, email, password):
        return User.objects.create_user(username=username, email=email, password=password)
    return _create_user

@pytest.mark.django_db
def test_project_list(api_client, create_user, create_project):
    user = create_user('testuser', 'test@user.com', 'testpassword')
    project = create_project('Test Project', 'Project Description')
    url = reverse('projects-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Project'

@pytest.mark.django_db
def test_project_create(api_client, create_user):
    user = create_user('testuser', 'testpassword')
    api_client.login(username='testuser', password='testpassword')
    url = reverse('project-list')
    data = {
        'name': 'New Project'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Project.objects.count() == 2
    assert Project.objects.last().name == 'New Project'

@pytest.mark.django_db
def test_item_list(api_client, create_user, create_project, create_item):
    user = create_user('testuser', 'testpassword')
    project = create_project(user, 'Test Project')
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
