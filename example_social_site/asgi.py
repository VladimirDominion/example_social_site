"""
ASGI config for example_social_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from chat.consumers import GroupListConsumer, GroupConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example_social_site.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^chat/groups/$", GroupListConsumer.as_asgi()),
            url(r"^chat/groups/(?P<group_id>\w+)/$", GroupConsumer.as_asgi()),
        ])
    ),
})
