from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied

from posts.models import Post
from posts.serialisers import PostSerializer
from posts.permissions import IsAuthor, PostPermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostPermission]

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action in ['list', 'retrieve']:
    #         permission_classes.append(AllowAny)
    #     elif self.action == 'create':
    #         permission_classes.append(IsAuthenticated)
    #     elif self.action in ['update', 'partial_update', 'destroy']:
    #         permission_classes.append(IsAuthor)
    #     else:
    #         permission_classes.append(IsAdminUser)
    #     return [permission() for permission in permission_classes]

    # def get_object(self):
    #     post = super().get_object()
    #     if self.action == 'retrieve' or post.author == self.request.user:
    #         return post
    #     raise PermissionDenied("Sorry, you don't have permissions")







