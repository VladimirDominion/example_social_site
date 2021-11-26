from rest_framework import serializers
from django.contrib.auth import get_user_model

from users import services as user_services


User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=20)
    password_repeat = serializers.CharField(min_length=8, max_length=20)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {
                    'email': 'User with this email already exist'
                }
            )
        return email

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError(
                {
                    'password': 'Password mismatch'
                }
            )
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
