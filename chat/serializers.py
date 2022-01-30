from rest_framework import serializers

from chat.models import ChatGroup, ChatMessage
from users.serializers import UserDetailSerializer


class ChatGroupSerializer(serializers.ModelSerializer):
    member = UserDetailSerializer(many=True)

    class Meta:
        model = ChatGroup
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(many=True)

    class Meta:
        model = ChatMessage
        exclude = ('group',)


class GroupCreateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=100)


class IdListSerializers(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())


class MessageSerializers(serializers.Serializer):
    message = serializers.CharField(max_length=250, min_length=2)