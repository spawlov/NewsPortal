from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, \
    ListView, DetailView

from .fiters import PostFilter
from .models import Post, Author, Comment, Category
from .form import PostingForm, UserForm
from .permissions import PermissionAndOwnerRequiredMixin, \
    ProfileOwnerRequiredMixin


class IndexView(ListView):
    model = Post
    ordering = '-date_pub'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class NewsView(ListView):
    queryset = Post.objects.filter(type_cat='NWS')
    ordering = '-date_pub'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class ArticlesView(ListView):
    queryset = Post.objects.filter(type_cat='ART')
    ordering = '-date_pub'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10


class PostDetails(DetailView):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'content'

    def get_context_data(self, **kwargs):
        context = super(PostDetails, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            post_id=context['content'].id
        )
        return context


class PostFind(ListView):
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
    permission_required = (
        'news.change_post',
    )
    form_class = PostingForm
    model = Post
    context_object_name = 'edit'
    template_name = 'edit.html'


class PostDelete(PermissionAndOwnerRequiredMixin, DeleteView):
    permission_required = (
        'news.delete_post',
    )
    model = Post
    context_object_name = 'delete'
    template_name = 'delete.html'
    success_url = reverse_lazy('news:index')


class AuthorEdit(ProfileOwnerRequiredMixin, UpdateView):
    permission_required = (
        'auth.change_user',
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
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect(f'/profile/{user.id}')
