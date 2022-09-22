from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from news.views import PostViewSet
from .yasg import urlpatterns as doc_urls

router = routers.DefaultRouter()
router.register(r'post', PostViewSet)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('news.urls')),
    path('api/v1/', include(router.urls)),
    # path('api/v1/postlist/', PostViewSet.as_view({'get': 'list'})),
    # path('api/v1/postlist/<int:pk>/', PostViewSet.as_view({'put': 'update'})),
    path('api/v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += doc_urls

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
