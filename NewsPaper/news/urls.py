from django.urls import path

from .views import IndexView, NewsView, PostDetails, ArticlesView, \
    PostCreate, PostFind, PostEdit, PostDelete, AuthorEdit, \
    request_upgrade_group

app_name = 'news'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('news/', NewsView.as_view(), name='news'),
    path('articles/', ArticlesView.as_view(), name='articles'),
    path('<int:pk>/', PostDetails.as_view(), name='detail'),
    path('create/', PostCreate.as_view(), name='create'),
    path('search/', PostFind.as_view(), name='search'),
    path('edit/<int:pk>/', PostEdit.as_view(), name='edit'),
    path('delete/<int:pk>/', PostDelete.as_view(), name='delete'),

    path('profile/<int:pk>/', AuthorEdit.as_view(), name='profile'),
    path('req_to_author/', request_upgrade_group, name='req_to_author')
]
