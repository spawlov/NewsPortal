from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author_post',
            'type_cat',
            'name',
            'content',
            'post_cat',
        ]
