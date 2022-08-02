from django.urls import path

from .views import IndexView, NewsView, PostDetails, ArticlesView, PostCreate, \
    PostFind

app_name = 'news'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('news/', NewsView.as_view(), name='news'),
    path('articles/', ArticlesView.as_view(), name='articles'),
    path('<int:pk>/', PostDetails.as_view(), name='detail'),
    path('posts/create/', PostCreate.as_view(), name='create'),
    path('posts/find/', PostFind.as_view(), name='find'),
]
