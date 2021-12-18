from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Post, PostComment, PostLike
from posts.serialisers import PostSerializer, PostCommentSerializer
from posts.permissions import IsAuthor, PostPermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('tags', 'comments', 'likes')
    serializer_class = PostSerializer
    permission_classes = [PostPermission]

    def get_permissions(self):
        permission_classes = []
        if self.action in ['list', 'retrieve', 'comments']:
            permission_classes.append(AllowAny)
        elif self.action in ['create', 'like', 'comment_create']:
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

    @action(methods=['GET'], detail=True)
    def comments(self, request, pk=None):
        post = self.get_object()
        comments_queryset = post.comments.all()
        serializer = PostCommentSerializer(comments_queryset, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True, serializer_class=PostCommentSerializer)
    def comment_create(self, request, pk=None):
        author = request.user
        post = self.get_object()
        data = request.data.copy()
        data['author'] = author.id
        data['post'] = post.id
        serializer = PostCommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(PostCommentSerializer(serializer.instance))

    @action(
        methods=['PATCH'],
        detail=True,
        serializer_class=PostCommentSerializer,
        url_path='comment_update/(?P<comment_id>[0-9]+)'
    )
    def comment_update(self, request, pk=None, comment_id=None):
        author = request.user
        comment = PostComment.objects.get(pk=comment_id)
        if comment.author != author:
            return Response({'message': "You can't edit this comment"}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostCommentSerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(PostCommentSerializer(serializer.instance))

    @action(
        methods=['DELETE'],
        detail=True,
        url_path='comment_delete/(?P<comment_id>[0-9]+)'
    )
    def comment_delete(self, request, pk=None, comment_id=None):
        author = request.user
        comment = PostComment.objects.get(pk=comment_id)
        if comment.author != author:
            return Response({'message': "You can't delete this comment"}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST'],
        detail=True,
        serializer_class=PostCommentSerializer,
        url_path='comment_add_child/(?P<comment_id>[0-9]+)'
    )
    def comment_add_child(self, request, pk=None, comment_id=None):
        pass

    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like, _ = PostLike.objects.get_or_create(author=user, post=post)
        return Response({'message': 'Thank you, for your like'})


class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all().select_related('post', 'parent', 'author')
    serializer_class = PostCommentSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action in ['list', 'retrieve']:
            permission_classes.append(AllowAny)
        elif self.action in ['create', ]:
            permission_classes.append(IsAuthenticated)
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsAuthor)
        else:
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]








