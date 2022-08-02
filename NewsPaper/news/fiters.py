from django_filters import FilterSet

from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'name': ['icontains'],
            # 'content': ['icontains'],
            'post_cat': ['exact'],
            'date_pub': ['gt'],
        }
