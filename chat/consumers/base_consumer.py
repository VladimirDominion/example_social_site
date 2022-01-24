from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.pydentic_models import ChannelsMessage
from chat.constants import ChatMessageStatus


class BaseChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user', None)
        if not user or not user.is_authenticated:
            await self._send_message(
                    event='error.message',
                    data='Login first, please',
                    status=ChatMessageStatus.ERROR
                )
            await self.close()
        await self.accept()

    async def _send_message(self, *, data, event, status):
        data = dict(event=event, data=data, status=status)
        await self.send_json(data)

    async def receive_json(self, content, **kwargs):
        try:
            content = ChannelsMessage(**content)
        except Exception:
            await self._send_message(
                event='error.message',
                data='Not valid data',
                status=ChatMessageStatus.ERROR
            )
            return
        event = f"event_{content['event'].replace('.', '_')}"
        data = content['data']
        method = getattr(self, event, None)
        if not method:
            await self._send_message(
                event='error.message',
                data='Method not found',
                status=ChatMessageStatus.ERROR
            )
            return
        await method(data)

    async def disconnect(self, code):
        pass

