from rest_framework import serializers

from Blog.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "content", "created_at", "post", "author")
