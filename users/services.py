from typing import Dict

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers


User = get_user_model()


def get_tokens_for_user(*, user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def sign_up_user(*, user_data: Dict):
    user = User.objects.create_user(email=user_data['email'], password=user_data['password'])
    return user


def login(*, user_credentials):
    user = authenticate(**user_credentials)
    if not user or not user.is_active:
        return
    return user


def change_password(user, password):
    user.set_password(password)
    user.save()
