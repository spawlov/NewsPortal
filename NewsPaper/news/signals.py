from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post

from .tasks import notify_subscribers_for_new_post


@receiver(m2m_changed, sender=Post)
def notify_for_new_post(sender, instance, action, **kwargs):

    # Добавление задания на отправку письма
    if action == 'post_add' and instance.__class__.__name__ == 'Post':
        notify_subscribers_for_new_post.apply_async(
            (instance.id, instance.name, instance.content),
            countdown=5,
        )
