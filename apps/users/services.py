from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from core.exceptions import InvalidCredentials


def authenticate_user(*, username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise InvalidCredentials()
    return user


def create_tokens_for_user(*, user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def login_user(*, username, password):
    user = authenticate_user(username=username, password=password)
    tokens = create_tokens_for_user(user=user)
    return user, tokens