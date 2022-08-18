import os

from django.contrib.sites.models import Site
from django.core import mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, PostCategory


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers_for_new_post(sender, instance, action, **kwargs):
    """Отправка письма подписчика при добавлении нового поста в категорию"""

    if action == 'post_add':

        # Формируем ссылку на новую статью
        # (на реальном сервере отредактировать)
        site = Site.objects.get_current()
        link = f'http://{site.domain}:8000{instance.get_absolute_url()}'

        # Формируем список рассылки
        mailing_list = list(
            PostCategory.objects.filter(
                post_id=instance.id
            ).select_related('category').values_list(
                'cat__subscribers__username',
                'cat__subscribers__first_name',
                'cat__subscribers__email',
                'cat__name',
            )
        )

        # Если список рассылки не пустой - отправляем каждому подписчику
        # индивидуальное письмо, за одно подключение к SMTP
        if any([all([len(mailing_list) == 1, mailing_list[0][2]]),
                len(mailing_list) > 1]):
            counter_mails = 0
            connection = None
            try:
                connection = mail.get_connection()
                connection.open()
            except Exception as e:
                print(e)
            else:
                for user, first_name, email, category in mailing_list:
                    if not first_name:
                        first_name = user
                    html_content = render_to_string(
                        'email/added_post.html',
                        {
                            'name': first_name,
                            'category': category,
                            'title': instance.name,
                            'content': instance.content,
                            'post_id': instance.id,
                            'link': link,
                            'site_name': site.name,
                        }
                    )
                    message = mail.EmailMultiAlternatives(
                        subject=f'{first_name}, '
                                f'новая статья в категории "{category}"',
                        from_email=os.getenv('EMAIL'),
                        to=[email],
                        connection=connection,
                    )
                    message.attach_alternative(html_content, 'text/html')
                    message.send()
                    counter_mails += 1
            finally:
                connection.close()
                # print(f'Sent {counter_mails} Emails')
