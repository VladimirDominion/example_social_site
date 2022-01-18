from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.pydentic_models import ChannelsMessage


class BaseChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user', None)
        if not user or not user.is_authenticated:
            await self.close()
        await self.accept()

    async def receive_json(self, content, **kwargs):
        try:
            content = ChannelsMessage(**content)
        except Exception:
            # send error message
            pass
        event = content['event'].replace('.', '_')
        data = content['data']
        method = getattr(self, event, None)
        if not method:
            pass  # send error message
        await method(data)

    async def disconnect(self, code):
        pass

