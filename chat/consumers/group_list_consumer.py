from typing import Dict

from channels.db import database_sync_to_async
from rest_framework.exceptions import ValidationError

from .base_consumer import BaseChatConsumer
from chat.models import ChatGroup
from chat.constants import ChatMessageStatus
from chat.serializers import ChatGroupSerializer, GroupCreateSerializer


class GroupListConsumer(BaseChatConsumer):
    # Event Handlers
    async def event_group_list(self, data):
        group_list = await database_sync_to_async(self.get_group_list)()
        await self._send_message(
            event='group.list',
            data=ChatGroupSerializer(group_list, many=True).data,
            status=ChatMessageStatus.SUCCESS
        )

    async def event_group_add(self, data):
        try:
            serializer = GroupCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            await self._send_message(
                event='group.add',
                data={'detail': str(e)},
                status=ChatMessageStatus.ERROR
            )
        else:
            group_json = await database_sync_to_async(
                self.group_create
            )(serializer.validated_data['name'])
            await self._send_message(
                event='group.add',
                data=group_json,
                status=ChatMessageStatus.SUCCESS
            )

    # Database Sync Methods

    def get_group_list(self):
        return ChatGroup.objects.filter(
            member=self.scope['user']
        )

    def group_create(self, group_name: str) -> Dict:
        new_group = ChatGroup.objects.create(name=group_name)
        new_group.member.add(self.scope['user'])
        return ChatGroupSerializer(new_group).data
