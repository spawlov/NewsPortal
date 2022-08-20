from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    verbose_name = 'Новостной портал'

    def ready(self):
        from . import signals
        signals.m2m_changed.connect(signals.notify_for_new_post)
