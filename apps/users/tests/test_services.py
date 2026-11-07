import pytest

from apps.users.services import authenticate_user, login_user
from apps.users.tests.factories import UserFactory
from core.exceptions import InvalidCredentials


@pytest.mark.django_db
def test_authenticate_user_success():
    user = UserFactory(username='testuser')
    result = authenticate_user(username='testuser', password='test12345')
    assert result == user


@pytest.mark.django_db
def test_authenticate_user_wrong_password():
    UserFactory(username='testuser')
    with pytest.raises(InvalidCredentials):
        authenticate_user(username='testuser', password='wrong')


@pytest.mark.django_db
def test_authenticate_user_unknown_username():
    with pytest.raises(InvalidCredentials):
        authenticate_user(username='nouser', password='test12345')


@pytest.mark.django_db
def test_login_user_returns_tokens():
    UserFactory(username='testuser')
    user, tokens = login_user(username='testuser', password='test12345')
    assert user.username == 'testuser'
    assert 'access' in tokens
    assert 'refresh' in tokens