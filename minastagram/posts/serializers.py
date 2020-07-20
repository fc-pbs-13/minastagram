from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from posts.models import Post, Comment


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CommentSerializer(ModelSerializer):
    # author = serializers.StringRelatedField()
    reply = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_date', 'post', 'reply', ]
        read_only_fields = ('post', 'author',)

    def get_reply(self, instance):
        # recursive
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data


class PostSerializer(ModelSerializer):
    comment = CommentSerializer(many=True, source='post_set', read_only=True)
    owner = serializers.StringRelatedField()
    like_users = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'owner', 'image', 'text', 'created_date', 'comment', 'like_users']

    def get_like_users(self, obj):
        return obj.like_users.count()
