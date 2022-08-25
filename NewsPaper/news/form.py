from django import forms

from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

from allauth.account.forms import SignupForm as BaseSignupForm
from allauth.socialaccount.forms import SignupForm as SocSignupForm

from .models import Post, Author


class PostingForm(forms.ModelForm):
    """Добавление публикации на сайт"""
    error_css_class = 'text-danger fw-semibold'

    class Meta:
        model = Post
        fields = [
            'type_cat',
            'name',
            'content',
            'content_image',
            'post_cat',
        ]
        widgets = {
            'type_cat': forms.Select(
                attrs={'class': 'form-select border-primary'}
            ),
            'name': forms.TextInput(
                attrs={'class': 'form-control border-primary'}
            ),
            'content': forms.Textarea(
                attrs={'class': 'form-control border-primary'}
            ),
            'content_image': forms.FileInput(
                attrs={'class': 'form-control border-primary'}
            ),
            'post_cat': forms.SelectMultiple(
                attrs={'class': 'form-select border-primary'}
            ),
        }



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
    """Форма профайла пользователя"""
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control border-primary'}
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control border-primary'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control border-primary'}
            ),
        }

def user_added_to_group(user):
    """Добавление нового пользователя в группу common"""
    common_group = Group.objects.get(name='common')
    common_group.user_set.add(user)
    Author.objects.create(
        author_user_id=User.objects.get(username=user).id
    )


class BasicSignupForm(BaseSignupForm):
    """Базовая форма регистрации allauth"""
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        user_added_to_group(user)
        return user


class SocialSignupForm(SocSignupForm):
    """Форма регистрации через провайдера allauth"""
    def save(self, request):
        user = super(SocialSignupForm, self).save(request)
        user_added_to_group(user)
        return user
