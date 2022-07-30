from django.views import generic
from .models import Post, Author, Comment


class IndexView(generic.ListView):
    model = Post
    ordering = '-date_pub'
    template_name = 'news.html'
    context_object_name = 'posts'


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
