from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver

from .models import Post, Category

from .tasks import notify_subscribers_for_new_post


@receiver(m2m_changed, sender=Post)
def notify_for_new_post(sender, instance, action, **kwargs):
    # Добавление задания на отправку письма
    if action == 'post_add' and instance.__class__.__name__ == 'Post':
        notify_subscribers_for_new_post.apply_async(
            (instance.id, instance.name, instance.content),
            countdown=300,
        )


@receiver(post_delete, sender=Category)
def clear_cache_navbar(sender, instance, **kwargs):
    key = make_template_fragment_key('navbar')
    cache.delete(key)


@receiver(post_delete, sender=Post)
def clear_cache_navbar(sender, instance, **kwargs):
    cache.delete(f'post-id-{instance.pk}')
