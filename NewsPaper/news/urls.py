from django.urls import path

from .views import IndexView, PostDetails

app_name = 'news'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', PostDetails.as_view(), name='detail'),
]
