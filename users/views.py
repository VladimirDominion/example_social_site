from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from users.permissions import IsOwner
from users import serializers as user_serializers
from users import services as user_services
from users.tasks import user_login


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter().prefetch_related()
    serializer_class = user_serializers.UserDetailSerializer
    ALLOWED_ACTIONS = ['login', 'sign_up']
    PROTECTED_ACTIONS = ['me', 'update', 'partial_update', 'change_password']

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

    @action(
        methods=['POST'],
        detail=False,
        serializer_class=user_serializers.LoginSerializer
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_credentials = serializer.validated_data
        user = user_services.login(user_credentials=user_credentials)
        if not user:
            return Response({'message': 'User with this credentials not found'}, status=status.HTTP_400_BAD_REQUEST)
        response_data = user_serializers.UserDetailSerializer(user).data
        response_data.update(user_services.get_tokens_for_user(user=user))
        user_login.applay_async(args=[1], queue='import_queue')
        return Response(response_data)

    @action(methods=['GET'], detail=False)
    def me(self, request):
        response_data = user_serializers.UserDetailSerializer(request.user).data
        return Response(response_data)

    @action(
        methods=['POST'],
        detail=False,
        serializer_class=user_serializers.ChangePasswordSerializer
    )
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_services.change_password(user=request.user, password=data['new_password'])
        return Response({'message': 'Password successfully changed'})

