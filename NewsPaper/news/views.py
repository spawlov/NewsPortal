from django.views import generic
from .models import Post, Author, Comment

from django.shortcuts import get_object_or_404

class IndexView(generic.ListView):
    model = Post
    ordering = '-date_pub'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5


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
