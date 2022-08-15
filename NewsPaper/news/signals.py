import os

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, PostCategory, CatSubscribers, Category


@receiver(m2m_changed, sender=Post)
def notify_subscribers_for_new_post(sender, instance, action, **kwargs):
    """Отправка письма подписчика при добавлении нового поста в категорию"""

    if action == 'post_add':

        # Формируем ссылку на новую статью
        site = Site.objects.get_current()
        link = f'http://{site.domain}:8000{instance.get_absolute_url()}'

        # Формируем список номеров категорий
        category_id = PostCategory.objects.filter(
            post=instance.id
        ).values_list('cat_id', flat=True)

        # Формируем списки получателей для каждой категории
        mailing_list = {}
        for cat_id in category_id:
            subscriber = CatSubscribers.objects.filter(
                category=cat_id
            ).values_list('subscriber', flat=True)

            cat_name = Category.objects.get(id=cat_id)

            email_list = User.objects.filter(
                id__in=subscriber).values_list('email', flat=True)

            mailing_list[str(cat_name)] = list(email_list)

        # Готовим письма для каждой категории и отправляем по спискам рассылки
        for category, mails in mailing_list.items():
            html_content = render_to_string(
                'email/added_post.html',
                {
                    'category': category,
                    'title': instance.name,
                    'content': instance.content,
                    'post_id': instance.id,
                    'link': link,
                }
            )
            message = EmailMultiAlternatives(
                subject=f'Новая статья в категории {category}',
                from_email=os.getenv('EMAIL'),
                to=mails,
            )
            message.attach_alternative(html_content, 'text/html')
            try:
                message.send()
            except Exception as e:
                print(e)
