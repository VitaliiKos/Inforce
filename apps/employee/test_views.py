import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.employee.models import Employee, UserProfile
from .factories import EmployeeFactory


# === FIXTURES ===

@pytest.fixture()
def api_client():
    """Returns an instance of the Django test APIClient."""
    return APIClient()


@pytest.fixture()
def user(db):
    """Creates and returns a test Employee user."""
    return EmployeeFactory()


@pytest.fixture()
def auth_headers(user):
    """Returns authorization headers for a given user using JWT access token."""
    refresh = RefreshToken.for_user(user)
    return {
        'HTTP_AUTHORIZATION': f'Bearer {refresh.access_token}',
    }


# === AUTHENTICATED TESTS ===

@pytest.mark.django_db
def test_employee_list(api_client, user, auth_headers):
    """Test that the employee list endpoint returns users except the current authenticated one."""
    other_user = EmployeeFactory()
    url = reverse('employee_list')

    response = api_client.get(url, **auth_headers)

    assert response.status_code == status.HTTP_200_OK
    emails = [emp['email'] for emp in response.data['data']]
    assert user.email not in emails
    assert other_user.email in emails


@pytest.mark.django_db
def test_employee_detail(api_client, user, auth_headers):
    """Test that the employee detail endpoint returns the correct user data."""
    url = reverse('employee_detail', args=[user.pk])
    response = api_client.get(url, **auth_headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == user.email


@pytest.mark.django_db
def test_employee_change_password(api_client, user, auth_headers):
    """Test that an authenticated user can successfully change their password."""
    url = reverse('employee_change_password')
    new_password = 'NewP@ssw0rd!'

    response = api_client.patch(url, {"password": new_password}, **auth_headers)

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.check_password(new_password)


@pytest.mark.django_db
def test_employee_delete_self(api_client, user, auth_headers):
    """Test that an authenticated user can delete their own account."""
    url = reverse('employee_delete')
    response = api_client.delete(url, **auth_headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Employee.objects.filter(id=user.id).exists()


@pytest.mark.django_db
def test_update_profile(api_client, user, auth_headers):
    """Test updating user's profile information with valid data."""
    UserProfile.objects.create(user=user, first_name='John', last_name='Doe', phone='0501112233')
    url = reverse('employee_profile_update')
    data = {
        'first_name': 'Updated',
        'last_name': 'Name',
        'phone': '0671234586'
    }

    response = api_client.patch(url, data, **auth_headers)

    assert response.status_code == status.HTTP_200_OK
    user.profile.refresh_from_db()
    assert user.profile.first_name == 'Updated'
    assert user.profile.phone == '0671234586'


# === UNAUTHENTICATED TESTS ===

@pytest.mark.django_db
@pytest.mark.parametrize("url_name, method, needs_pk", [
    ('employee_list', 'get', False),
    ('employee_detail', 'get', True),
    ('employee_profile_update', 'patch', False),
    ('employee_change_password', 'patch', False),
    ('employee_delete', 'delete', False),
])
def test_unauthorized_access(api_client, url_name, method, needs_pk):
    """Test that endpoints correctly return 401 for unauthorized access."""
    user = EmployeeFactory() if needs_pk else None
    kwargs = {'pk': user.pk} if needs_pk else None
    url = reverse(url_name, kwargs=kwargs)
    response = getattr(api_client, method)(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# === EDGE CASES ===

@pytest.mark.django_db
def test_employee_detail_not_found(api_client, auth_headers):
    """Test accessing a non-existent employee returns 404."""
    url = reverse('employee_detail', args=[999])  # Non-existent ID
    response = api_client.get(url, **auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_profile_invalid_data(api_client, user, auth_headers):
    """Test that invalid profile update data returns 400 Bad Request."""
    UserProfile.objects.create(user=user, first_name='Test', last_name='User')
    url = reverse('employee_profile_update')
    data = {'first_name': '123Invalid'}  # Invalid name format
    response = api_client.patch(url, data, format='json', **auth_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_change_password_weak(api_client, user, auth_headers):
    """Test changing password to a weak one returns 400 Bad Request."""
    url = reverse('employee_change_password')
    data = {'password': '123'}  # Too weak
    response = api_client.patch(url, data, format='json', **auth_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
