from django.urls import path

from .views import IndexView, NewsView, PostDetails, ArticlesView, PostCreate, \
    PostFind, PostEdit, PostDelete

app_name = 'news'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('news/', NewsView.as_view(), name='news'),
    path('articles/', ArticlesView.as_view(), name='articles'),
    path('<int:pk>/', PostDetails.as_view(), name='detail'),
    path('create/', PostCreate.as_view(), name='create'),
    path('find/', PostFind.as_view(), name='find'),
    path('edit/<int:pk>/', PostEdit.as_view(), name='edit'),
    path('delete/<int:pk>/', PostDelete.as_view(), name='delete'),
]
