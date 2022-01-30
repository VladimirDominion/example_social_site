from typing import Dict, List

from channels.db import database_sync_to_async
from rest_framework.exceptions import ValidationError

from .base_consumer import BaseChatConsumer
from chat.models import ChatGroup, ChatMessage
from chat.constants import ChatMessageStatus
from chat import serializers as chat_serializers
from users.models import User


class GroupConsumer(BaseChatConsumer):

    async def connect(self):
        await super(GroupConsumer, self).connect()
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group = await database_sync_to_async(self.get_group_by_id)(self.group_id)
        await self.channel_layer.group_add(
            self.group.get_channel_name(self.group_id), self.channel_name
        )

    async def disconnect(self, code):
        await super(GroupConsumer, self).disconnect(code)
        await self.channel_layer.group_discard(
            self.group.get_channel_name(self.group_id), self.channel_name
        )

    # Event Handlers
    async def event_add_members(self, data):
        try:
            serializer = chat_serializers.IdListSerializers(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            await self._send_message(
                event='add.members',
                data={'detail': str(e)},
                status=ChatMessageStatus.ERROR
            )
        else:
            group_json = await database_sync_to_async(
                self.add_members
            )(serializer.validated_data['ids'])
            await self._send_message(
                event='add.members',
                data=group_json,
                status=ChatMessageStatus.SUCCESS
            )

    async def event_list_messages(self, data):
        messages_json = await database_sync_to_async(
            self.get_list_messages
        )(self.group_id)
        await self._send_message(
            event='list.messages',
            data=messages_json,
            status=ChatMessageStatus.SUCCESS
        )

    async def event_send_message(self, data):
        try:
            serializer = chat_serializers.MessageSerializers(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            await self._send_message(
                event='send.message',
                data={'detail': str(e)},
                status=ChatMessageStatus.ERROR
            )
        else:
            json_message = await database_sync_to_async(
                self.add_message
            )(serializer.validated_data['message'])
            await self.channel_layer.group_send(
                self.get_group_name(self.group_id),
                {
                    'event': 'send.message',
                    'data': json_message,
                    'status': ChatMessageStatus.SUCCESS
                }
            )

    @classmethod
    def get_group_by_id(cls, group_id: int) -> ChatGroup:
        return ChatGroup.objects.get(pk=group_id)

    @classmethod
    def add_members(cls, group: ChatGroup, members_ids: List[int]) -> Dict:
        members = User.objects.filter(id__in=members_ids)
        group.member.add(*members)
        return chat_serializers.ChatGroupSerializer(group).data

    @classmethod
    def get_list_messages(cls, group_id):
        messages = ChatMessage.objects.filter(
            group_id=group_id
        ).select_related('author').order_by('-id')
        return chat_serializers.ChatMessageSerializer(messages, many=True).data

    def add_message(self, message):
        author = self.scope['user']
        group = self.group
        created_message = ChatMessage.objects.create(
            author=author, group=group, message=message
        )
        return chat_serializers.ChatMessageSerializer(created_message).data

    