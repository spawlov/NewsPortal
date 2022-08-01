from django.urls import path

from .views import IndexView, NewsView, PostDetails, ArticlesView

app_name = 'news'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('news/', NewsView.as_view(), name='news'),
    path('articles/', ArticlesView.as_view(), name='articles'),
    path('<int:pk>/', PostDetails.as_view(), name='detail'),
]
