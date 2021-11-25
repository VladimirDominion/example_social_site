from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action

from users.models import User
from users.permissions import IsOwner
from users import serializers as user_serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter().prefetch_related()
    ALLOWED_ACTIONS = ['login', 'sign-up']
    PROTECTED_ACTIONS = ['me', 'update', 'partial_update']

    def get_permissions(self):
        permission_classes = []
        if self.action in self.ALLOWED_ACTIONS:
            permission_classes.append(AllowAny)
        elif self.action in self.PROTECTED_ACTIONS:
            permission_classes.append(IsOwner)
        else:
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def get_object(self):
        return self.get_queryset().first()

    # ALLOWED_ACTIONS
    @action(
        methods=['POST'],
        detail=False,
        url_path='/users/sign-up/',
        serializer_class=user_serializers.SignUpSerializer
    )
    def sign_up(self, request):
        serializer = user_serializers.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
