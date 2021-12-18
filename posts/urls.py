from rest_framework import routers

from posts.views import PostViewSet, PostCommentViewSet

posts_router = routers.SimpleRouter()
posts_router.register(r'posts', PostViewSet)
posts_router.register(r'comments', PostCommentViewSet)


urlpatterns = posts_router.urls
