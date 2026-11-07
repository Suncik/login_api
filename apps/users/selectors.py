from django.shortcuts import get_object_or_404

from .models import User


def get_user_by_id(*, user_id):
    return get_object_or_404(User, pk=user_id)