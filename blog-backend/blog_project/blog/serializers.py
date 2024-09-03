# serializers.py

from rest_framework import serializers
from .models import Post, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author, created = User.objects.get_or_create(**author_data)
        post = Post.objects.create(author=author, **validated_data)
        return post

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)
        if author_data:
            author, created = User.objects.get_or_create(**author_data)
            instance.author = author
        
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
