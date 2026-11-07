import pytest
from rest_framework.test import APIClient

from apps.users.tests.factories import UserFactory

LOGIN_URL = '/api/auth/login/'
ME_URL = '/api/auth/me/'


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_login_success(client):
    UserFactory(username='testuser', email='test@example.com')
    response = client.post(
        LOGIN_URL,
        {'username': 'testuser', 'password': 'test12345'},
        format='json',
    )
    assert response.status_code == 200
    assert response.data['message'] == 'Login successful'
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert response.data['user']['username'] == 'testuser'
    assert response.data['user']['email'] == 'test@example.com'


@pytest.mark.django_db
def test_login_wrong_password(client):
    UserFactory(username='testuser')
    response = client.post(
        LOGIN_URL,
        {'username': 'testuser', 'password': 'wrong'},
        format='json',
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_login_unknown_username(client):
    response = client.post(
        LOGIN_URL,
        {'username': 'nouser', 'password': 'test12345'},
        format='json',
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_login_empty_fields(client):
    response = client.post(
        LOGIN_URL,
        {'username': '', 'password': ''},
        format='json',
    )
    assert response.status_code == 400
    assert 'username' in response.data
    assert 'password' in response.data


@pytest.mark.django_db
def test_me_without_token(client):
    response = client.get(ME_URL)
    assert response.status_code == 401


@pytest.mark.django_db
def test_me_with_token(client):
    UserFactory(username='testuser', email='test@example.com')
    login = client.post(
        LOGIN_URL,
        {'username': 'testuser', 'password': 'test12345'},
        format='json',
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
    response = client.get(ME_URL)
    assert response.status_code == 200
    assert response.data['username'] == 'testuser'
    assert response.data['email'] == 'test@example.com'