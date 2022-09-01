from datetime import timedelta
from random import randint
from icecream import ic

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_list_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from django.utils import timezone

from django.views.generic import CreateView, DeleteView, UpdateView, \
    ListView, DetailView

from .fiters import PostFilter
from .models import Post, Author, Comment, Category, PostCategory
from .form import PostingForm, UserForm
from .permissions import PermissionAndOwnerRequiredMixin, \
    ProfileOwnerRequiredMixin
from django.conf import settings


class IndexView(ListView):
    """Вывод всех новостей и статей"""
    queryset = Post.objects.select_related().all().order_by('-date_pub')[:10]
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем контекст для двух случайных статей (на будущее)
        # first_id = second_id = 1
        # id_list = list(Post.objects.all().values_list('id', flat=True))
        # while not Post.objects.filter(id__in=[first_id, second_id]).exists():
        #     first_id = second_id = randint(id_list[0], id_list[-1])
        #     while first_id == second_id:
        #         second_id = randint(id_list[0], id_list[-1])
        # print(first_id, second_id)
        # context['first'] = Post.objects.get(pk=first_id)
        # context['second'] = Post.objects.get(pk=second_id)

        return context


# class NewsView(ListView):
#     """Вывод контента из раздела Новости"""
#     queryset = Post.objects.filter(type_cat='NWS').select_related()
#     ordering = '-date_pub'
#     template_name = 'news.html'
#     context_object_name = 'news'
#     paginate_by = 10
#
#
# class ArticlesView(ListView):
#     """Вывод контента из раздела Статьи"""
#     queryset = Post.objects.filter(type_cat='ART').select_related()
#     ordering = '-date_pub'
#     template_name = 'articles.html'
#     context_object_name = 'articles'
#     paginate_by = 10


class CategoryView(ListView):
    """Вывод статей определенной категории"""
    queryset = Post.objects.all()[:1]
    template_name = 'category.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверяем запрос на корректность
        cat_id = self.kwargs['pk']
        get_list_or_404(PostCategory, cat_id=cat_id)
        # Получаем имя категории
        context['cat_name'] = PostCategory.objects.filter(
            cat=cat_id
        ).values_list('cat__name', flat=True)[0]
        # Получаем кэшируемый контекст для категории
        context['posts'] = cache.get_or_set(
            f'category-id-{cat_id}',
            Post.objects.select_related().filter(
                post_cat__exact=cat_id
            ).order_by('-date_pub'),
            600
        )
        # Добавление контекста для подписки
        context['post_category'] = PostCategory.objects.filter(
            cat=cat_id
        ).select_related()[:1]
        context['is_subscribed'] = Category.objects.filter(
            subscribers=self.request.user.id
        ).values_list('name', flat=True)
        return context

class PostDetails(DetailView):
    """Вывод выбранной статьи"""
    queryset = Post.objects.all().select_related()
    template_name = 'detail.html'
    context_object_name = 'content'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-id-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-id-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Подтягиваем комментарии к статье
        context['comments'] = Comment.objects.select_related().filter(
            post_id=self.kwargs['pk']
        )
        # Добавление контекста для подписки
        context['post_category'] = PostCategory.objects.filter(
            post_id=self.object.pk
        ).select_related()
        context['is_subscribed'] = Category.objects.filter(
            subscribers=self.request.user.id
        ).values_list('name', flat=True)
        return context


class PostFind(ListView):
    """Поиск по сайту"""
    model = Post
    ordering = '-date_pub'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.postfilter = PostFilter(self.request.GET, queryset)
        return self.postfilter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['postfilter'] = self.postfilter
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    """Добавление Статьи/Новости"""
    permission_required = (
        'news.add_post',
    )
    context_object_name = 'create'
    form_class = PostingForm
    model = Post
    template_name = 'edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Добавляем текущего пользователя в форму
        self.object.author_post = Author.objects.get(
            author_user=self.request.user
        )
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверяем количество постов автора за текущие сутки
        limit = settings.DAILY_POST_LIMIT
        context['limit'] = limit
        last_day = timezone.now() - timedelta(days=1)
        posts_day_count = Post.objects.filter(
            author_post__author_user=self.request.user,
            date_pub__gte=last_day,
        ).count()
        context['count'] = posts_day_count
        context['post_limit'] = posts_day_count < limit
        return context


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
        # Добавляем подписчика в базу и
        # отправляем письмо об успешной подписке
        category.subscribers.add(user)
        html_content = render_to_string(
            'email/cat_subscribe.html',
            {
                'user': user,
                'category': category.name,
            }
        )
        message = EmailMultiAlternatives(
            subject=f'{user}, подписка на новости {category.name} оформлена!',
            from_email=settings.EMAIL,
            to=[user.email],
        )
        message.attach_alternative(html_content, 'text/html')
        try:
            message.send()
        except Exception as e:
            print(e)
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


@login_required
def like_article(request, pk):
    liked_post = Post.objects.get(pk=pk)
    author_id = liked_post.author_post.id
    author = Author.objects.get(pk=author_id)
    liked_post.like()
    author.update_rate()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def dislike_article(request, pk):
    disliked_post = Post.objects.get(pk=pk)
    author_id = disliked_post.author_post.id
    author = Author.objects.get(pk=author_id)
    disliked_post.dislike()
    author.update_rate()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
