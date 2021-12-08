from rest_framework import routers

from posts.views import PostViewSet

posts_router = routers.SimpleRouter()
posts_router.register(r'posts', PostViewSet)


urlpatterns = posts_router.urls
