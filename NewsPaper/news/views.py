from datetime import datetime, timedelta

from django.views import generic

from .fiters import PostFilter
from .models import Post, Author, Comment, Category
from .form import PostForm


class IndexView(generic.ListView):
    model = Post
    ordering = '-date_pub'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class NewsView(generic.ListView):
    queryset = Post.objects.filter(type_cat='NWS')
    ordering = '-date_pub'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5


class ArticlesView(generic.ListView):
    queryset = Post.objects.filter(type_cat='ART')
    ordering = '-date_pub'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 5


class PostDetails(generic.DetailView):
    model = Post
    template_name = 'nws_art.html'
    context_object_name = 'content'

    def get_context_data(self, **kwargs):
        context = super(PostDetails, self).get_context_data(**kwargs)
        context['author'] = Author.objects.get(
            id=context['content'].author_post_id
        )
        context['comments'] = Comment.objects.filter(
            post_id=context['content'].id
        )
        return context


class PostFind(generic.ListView):
    model = Post
    template_name = 'find.html'
    context_object_name = 'find'
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


class PostCreate(generic.CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create.html'
