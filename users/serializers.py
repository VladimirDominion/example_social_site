from rest_framework import serializers


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=20)
    password_repeat = serializers.CharField(min_length=8, max_length=20)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError(
                {
                    'password': 'Password mismatch'
                }
            )
        return attrs
