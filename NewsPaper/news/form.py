from django import forms
from django.core.exceptions import ValidationError

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

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        name = cleaned_data.get('name')

        if content is not None and len(content) < 500:
            raise ValidationError({
                'content': 'Содержание не может быть менее 500 символов'
            })

        if name == content:
            raise ValidationError(
                'Содержание не должно быть идентично названию'
            )

        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data['name']
        if name[0].islower():
            raise ValidationError(
                'Название должно начинаться с заглавной буквы'
            )
        return name
