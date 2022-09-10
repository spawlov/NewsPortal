from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    verbose_name = _('Новостной портал')

    def ready(self):
        from . import signals
        signals.m2m_changed.connect(signals.notify_for_new_post)
