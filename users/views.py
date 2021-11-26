from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from users.permissions import IsOwner
from users import serializers as user_serializers
from users import services as user_services


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter().prefetch_related()
    ALLOWED_ACTIONS = ['login', 'sign_up']
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
        url_path='users/sign-up',
        serializer_class=user_serializers.SignUpSerializer
    )
    def sign_up(self, request):
        serializer = user_serializers.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        user = user_services.sign_up_user(user_data=user_data)
        response_data = user_serializers.UserDetailSerializer(user).data
        response_data.update(user_services.get_tokens_for_user(user=user))
        return Response(response_data, status=status.HTTP_201_CREATED)

    def login(self, request):
        """
        1. Создать сериалайзер
        2. Валидировать данные
        3. Получить юзера
        :param request:
        :return:
        """
