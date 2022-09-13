from django.urls import path

from .views import IndexView, PostDetails, PostCreate, PostFind, PostEdit, PostDelete, \
    AuthorEdit, request_upgrade_group, subscribe_category, unsubscribe_category, \
    CategoryView, like_article, dislike_article, ArchiveView, set_timezone, \
    set_local_for_user

app_name = 'news'
urlpatterns = [
    # Classes views
    path('', IndexView.as_view(), name='index'),
    # path('news/', NewsView.as_view(), name='news'),
    # path('articles/', ArticlesView.as_view(), name='articles'),
    path(
        'caterory/<int:pk>/', CategoryView.as_view(),
        name='category'
    ),
    path(
        'archive/<int:year>/<int:month>/', ArchiveView.as_view(),
        name='archive'
    ),
    path('<int:pk>/', PostDetails.as_view(), name='detail'),
    path('create/', PostCreate.as_view(), name='create'),
    path('search/', PostFind.as_view(), name='search'),
    path('edit/<int:pk>/', PostEdit.as_view(), name='edit'),
    path('delete/<int:pk>/', PostDelete.as_view(), name='delete'),
    path('profile/<int:pk>/', AuthorEdit.as_view(), name='profile'),
    # Functions views
    path('req_to_author/', request_upgrade_group, name='req_to_author'),
    path('subscribe_cat/<int:post_cat>/', subscribe_category),
    path('unsubscribe_cat/<int:post_cat>/', unsubscribe_category),
    path('set_tz/', set_timezone),
    path('save_local/', set_local_for_user),

    path('like_post/<int:pk>/', like_article),
    path('dislike_post/<int:pk>/', dislike_article),
]
