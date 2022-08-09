from django import forms

from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

from allauth.account.forms import SignupForm as BaseSignupForm
from allauth.socialaccount.forms import SignupForm as SocSignupForm

from .models import Post, Author


class PostingForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
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


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class BasicSignupForm(BaseSignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        Author.objects.create(
            author_user_id=User.objects.get(username=user).id
        )
        return user


class SocialSignupForm(SocSignupForm):

    def save(self, request):
        user = super(SocialSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        Author.objects.create(
            author_user_id=User.objects.get(username=user).id
        )
        return user
