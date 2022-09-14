from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['pk', 'name_ru', 'name_en', 'date_pub']
