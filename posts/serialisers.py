from rest_framework import serializers

from posts.models import Post, PostComment


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, post):
        request = self.context.get('request', None)
        if not request:
            return False
        user = request.user
        if not user.is_authenticated:
            return False
        if post.likes.filter(author=user).exists():
            return True
        return False

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


