import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, \
    ListView, DetailView
from icecream import ic

from .fiters import PostFilter
from .models import Post, Author, Comment, Category, PostCategory
from .form import PostingForm, UserForm
from .permissions import PermissionAndOwnerRequiredMixin, \
    ProfileOwnerRequiredMixin


class IndexView(ListView):
    """Основная вьюшка - вывод всех новостей и статей"""
    model = Post
    ordering = '-date_pub'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class NewsView(ListView):
    """Вывод контента из раздела Новости"""
    queryset = Post.objects.filter(type_cat='NWS')
    ordering = '-date_pub'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class ArticlesView(ListView):
    """Вывод контента из раздела Статьи"""
    queryset = Post.objects.filter(type_cat='ART')
    ordering = '-date_pub'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10


class PostDetails(DetailView):
    """Вывод выбранной статьи"""
    model = Post
    template_name = 'detail.html'
    context_object_name = 'content'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Подтягиваем комментарии к статье
        context['comments'] = Comment.objects.filter(
            post_id=context['content'].id
        )
        # Добавление контекста для подписки
        context['category'] = PostCategory.objects.filter(
            post_id=self.object.pk
        )
        context['is_subscribed'] = Category.objects.filter(
            subscribers=self.request.user.id
        ).values_list('name', flat=True)

        return context


class PostFind(ListView):
    """Поиск по сайту"""
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.postfilter = PostFilter(self.request.GET, queryset)
        return self.postfilter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['postfilter'] = self.postfilter
        context['category'] = Category.objects.all()
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    """Добавление Статьи/Новости"""
    permission_required = (
        'news.add_post',
    )

    form_class = PostingForm
    model = Post
    template_name = 'edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author_post = Author.objects.get(
            author_user=self.request.user
        )
        self.object.save()
        return super().form_valid(form)


class PostEdit(PermissionAndOwnerRequiredMixin, UpdateView):
    """Изменение Статьи/Новости"""
    # Используется доработанный миксин - с контролем владельца
    permission_required = (
        'news.change_post',
    )
    form_class = PostingForm
    model = Post
    context_object_name = 'edit'
    template_name = 'edit.html'


class PostDelete(PermissionAndOwnerRequiredMixin, DeleteView):
    """Удаление Статьи/Новости"""
    # Используется доработанный миксин - с контролем владельца
    permission_required = (
        'news.delete_post',
    )
    model = Post
    context_object_name = 'delete'
    template_name = 'delete.html'
    success_url = reverse_lazy('news:index')


class AuthorEdit(ProfileOwnerRequiredMixin, UpdateView):
    """Редактирование профиля пользователя"""
    # Используется доработанный миксин - с контролем владельца
    permission_required = (
        'auth.change_user',
        'account.change_emailaddress',
    )
    form_class = UserForm
    model = User
    context_object_name = 'profile'
    template_name = 'profile.html'
    success_url = reverse_lazy('news:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = \
            self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def request_upgrade_group(request):
    """Добавление пользователя в группу authors"""
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect(f'/profile/{user.id}')


@login_required
def subscribe_category(request, post_cat):
    """Подписка на новости в категории"""
    user = request.user
    category = Category.objects.get(pk=post_cat)
    is_subscribed = category.subscribers.filter(id=user.id).exists()
    if not is_subscribed:
        #  Добавляем подписчика в базу и
        # отправляем письмо об успешной подписке
        category.subscribers.add(user)
        try:
            send_mail(
                subject=f'{user}, подписка на новости {category.name} '
                        f'оформлена!',
                message=f'{user}, '
                        f'Вы подписались на рассылку новостей сайта '
                        f'"Paper News".\n'
                        f'После публикации новой статьи или новости в '
                        f'категории {category.name} - Вам придет письмо.\n\n'
                        f'С уважением, администрация сайта "News Paper"',
                from_email=os.getenv('EMAIL'),
                recipient_list=[user.email]
            )
        except Exception as e:
            ic(e)
        finally:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_category(request, post_cat):
    """Отписка от рассылки новостей в категории"""
    user = request.user
    category = Category.objects.get(pk=post_cat)
    is_subscribed = category.subscribers.filter(id=user.id).exists()
    if is_subscribed:
        category.subscribers.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
