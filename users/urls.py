from rest_framework import routers

from users.views import UserViewSet

user_router = routers.SimpleRouter()
user_router.register(r'users', UserViewSet)


urlpatterns = user_router.urls
