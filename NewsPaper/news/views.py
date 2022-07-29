from django.views import generic
from . import models
from .models import Post


class IndexView(generic.ListView):
    model = Post
    ordering = '-date_pub'
    template_name = 'news.html'
    context_object_name = 'posts'


class PostDetails(generic.DetailView):
    model = Post
    template_name = 'nws_art.html'
    context_object_name = 'content'
