from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from chat.constants import ChatMessageStatus
from chat.serializers import MessageSerializers

channel_layer = get_channel_layer()


class ChatGroup(models.Model):
    name = models.CharField(max_length=200, default='')
    member = models.ManyToManyField("users.User", blank=True)

    @classmethod
    def get_channel_name(cls, group_id):
        return f'group_{group_id}'


class ChatMessage(LifecycleModelMixin, models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    message = models.TextField(default="")

    def get_channel_message(self):
        return {
            'event': 'send.message',
            'data': MessageSerializers(self).data,
            'status': ChatMessageStatus.SUCCESS
        }

    @hook(AFTER_CREATE)
    def send_broadcast(self):
        async_to_sync(channel_layer.group_send)(
            self.group.get_channel_name(self.group.id),
            self.get_channel_message()
        )

