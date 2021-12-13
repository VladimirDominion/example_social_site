from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

from posts.models import Post
from posts.serialisers import PostSerializer
from posts.permissions import IsAuthor, PostPermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostPermission]

    def get_permissions(self):
        permission_classes = []
        if self.action in ['list', 'retrieve']:
            permission_classes.append(AllowAny)
        elif self.action in ['create', 'like']:
            permission_classes.append(IsAuthenticated)
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsAuthor)
        else:
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['request'] = self.request
        return data

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        pass







