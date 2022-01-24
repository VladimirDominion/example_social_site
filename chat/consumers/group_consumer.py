from channels.db import database_sync_to_async

from .base_consumer import BaseChatConsumer
from chat.models import ChatGroup
from chat.constants import ChatMessageStatus
from chat.serializers import ChatGroupSerializer


class GroupConsumer(BaseChatConsumer):
    async def event_group_list(self, *args, **kwargs):
        group_list = await database_sync_to_async(self.get_group_list)()
        await self._send_message(
            event='group.list',
            data=ChatGroupSerializer(group_list, many=True).data,
            status=ChatMessageStatus.SUCCESS
        )

    def get_group_list(self):
        return ChatGroup.objects.filter(
            member=self.scope['user']
        )