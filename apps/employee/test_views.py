import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.employee.models import Employee
from .factories import EmployeeFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_employee():
    return EmployeeFactory


@pytest.fixture
def user(db, create_employee):
    user = create_employee(email='user@example.com', password='password123')
    return user


@pytest.fixture
def auth_headers(user):
    refresh = RefreshToken.for_user(user)
    return {
        'HTTP_AUTHORIZATION': f'Bearer {refresh.access_token}',
    }


@pytest.mark.django_db
def test_register_employee(api_client):
    url = reverse('auth_register')
    data = {
        'email': 'newuser@example.com',
        'password': 'newpassword123',
        'first_name': 'New',
        'last_name': 'User'
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert Employee.objects.filter(email='newuser@example.com').exists()


@pytest.mark.django_db
def test_login_employee(api_client, user):
    url = reverse('auth_login')
    data = {
        'email': user.email,
        'password': 'password123'
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_get_me(api_client, user, auth_headers):
    url = reverse('auth_me')
    response = api_client.get(url, **auth_headers)
    assert response.status_code == 200
    assert response.data['email'] == user.email


@pytest.mark.django_db
def test_refresh_token(api_client, user):
    refresh = RefreshToken.for_user(user)
    url = reverse('auth_refresh')
    data = {
        'refresh': str(refresh)
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert 'access' in response.data
