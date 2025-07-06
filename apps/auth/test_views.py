import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.employee.models import Employee, UserProfile
from apps.employee.factories import EmployeeFactory
from utils.services.jwt_service import ActivateToken, JWTService


# === FIXTURES ===

@pytest.fixture()
def api_client():
    """Returns an instance of the Django test APIClient."""
    return APIClient()


@pytest.fixture()
def google_mock_data():
    """Returns mocked data returned from Google OAuth."""
    return {
        'email': 'googleuser@example.com',
        'given_name': 'Google',
        'family_name': 'User',
        'phone_number': '+380991112233',
    }


# === AUTH TESTS ===

@pytest.mark.django_db
def test_register_employee(api_client):
    """Test registering a new employee account."""
    url = reverse('auth_register')
    data = {
        'email': 'newuser@example.com',
        'password': 'P@ssword123',
        'profile': {'first_name': 'Test', 'last_name': 'User'}
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert Employee.objects.filter(email='newuser@example.com').exists()


@pytest.mark.django_db
def test_register_duplicate_email(api_client):
    """Test registering with an email that already exists fails."""
    EmployeeFactory(email='duplicate@example.com')
    url = reverse('auth_register')
    data = {
        'email': 'duplicate@example.com',
        'password': 'P@ssword123',
        'profile': {'first_name': 'a', 'last_name': 'b'}
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_register_invalid_password(api_client):
    """Test password validation during registration."""
    url = reverse('auth_register')
    data = {
        'email': 'user@example.com',
        'password': 'short',
        'profile': {'first_name': 'a', 'last_name': 'b'}
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_employee(api_client):
    """Test successful login returns access and refresh tokens."""
    user = EmployeeFactory(email='login@example.com', password='P@ssword123')
    url = reverse('auth_login')
    data = {'email': 'login@example.com', 'password': 'P@ssword123'}
    response = api_client.post(url, data)

    assert response.status_code == 200
    assert 'access' in response.data and 'refresh' in response.data


@pytest.mark.django_db
def test_login_wrong_password(api_client):
    """Test login fails with incorrect password."""
    user = EmployeeFactory(email='user@example.com', password='CorrectPass123')
    url = reverse('auth_login')
    data = {'email': 'user@example.com', 'password': 'WrongPass'}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_login_inactive_user(api_client):
    """Test inactive users cannot log in."""
    user = EmployeeFactory(email='inactive@example.com', password='P@ssword123', is_active=False)
    url = reverse('auth_login')
    data = {'email': user.email, 'password': 'P@ssword123'}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_refresh_token(api_client):
    """Test refresh token endpoint returns new access token."""
    user = EmployeeFactory()
    refresh = RefreshToken.for_user(user)
    url = reverse('auth_refresh')
    response = api_client.post(url, {'refresh': str(refresh)})

    assert response.status_code == 200
    assert 'access' in response.data


@pytest.mark.django_db
def test_auth_me(api_client):
    """Test authenticated user info retrieval."""
    user = EmployeeFactory()
    access = RefreshToken.for_user(user).access_token
    url = reverse('auth_me')
    response = api_client.get(url, HTTP_AUTHORIZATION=f'Bearer {access}')

    assert response.status_code == 200
    assert response.data['email'] == user.email


# === GOOGLE OAUTH TESTS ===

@pytest.mark.django_db
@patch('apps.auth.serializers.id_token.verify_oauth2_token')
def test_google_oauth_new_user(mock_verify_oauth, api_client, google_mock_data):
    """Test creating new user via Google OAuth login."""
    mock_verify_oauth.return_value = google_mock_data
    url = reverse('auth0_google')
    response = api_client.post(url, {'credential': 'valid_token'})

    assert response.status_code == 200
    user = Employee.objects.get(email=google_mock_data['email'])
    assert user.profile.first_name == 'Google'
    assert 'access' in response.data and 'refresh' in response.data


@pytest.mark.django_db
@patch('apps.auth.serializers.id_token.verify_oauth2_token')
def test_google_oauth_existing_user(mock_verify_oauth, api_client, google_mock_data):
    """Test existing user logging in via Google OAuth doesn't create duplicate."""
    existing_user = EmployeeFactory(email=google_mock_data['email'])
    UserProfile.objects.create(user=existing_user, first_name='Existing', last_name='User')
    mock_verify_oauth.return_value = google_mock_data

    url = reverse('auth0_google')
    response = api_client.post(url, {'credential': 'valid_token'})

    assert response.status_code == 200
    assert Employee.objects.count() == 1
    assert 'access' in response.data and 'refresh' in response.data


@pytest.mark.django_db
@patch('apps.auth.serializers.id_token.verify_oauth2_token', side_effect=ValueError("Invalid token"))
def test_google_oauth_invalid_token(mock_verify, api_client):
    """Test handling of invalid Google OAuth token."""
    url = reverse('auth0_google')
    response = api_client.post(url, {'credential': 'invalid_token'})

    assert response.status_code == 400
    assert 'credential' in response.data


# === ACCOUNT ACTIVATION ===

@pytest.mark.django_db
def test_activate_user_valid_token(api_client):
    """Test user activation using valid activation token."""
    user = EmployeeFactory(is_active=False)
    token = JWTService.create_token(user, ActivateToken)
    url = reverse('auth_users_activate', kwargs={'token': token})
    response = api_client.get(url)

    user.refresh_from_db()
    assert response.status_code == 200
    assert user.is_active is True
