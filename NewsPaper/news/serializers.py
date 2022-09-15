from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author_post = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = "__all__"
