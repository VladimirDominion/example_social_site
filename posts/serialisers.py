from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        instance = super().create(validated_data)
        for tag in tags:
            instance.tags.add(tag)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)
        return instance


