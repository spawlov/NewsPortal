import os

from django.contrib.auth.models import User
from django.core import mail
from django.template.loader import render_to_string

from datetime import timedelta

from django.contrib.sites.models import Site
from django.utils import timezone

from .models import Post, CatSubscribers, Category


def weekly_notify_for_new_posts():
    # Формируем ссылку для письма
    site = Site.objects.get_current()
    link = f'http://{site.domain}:8000/'

    # Получаем список категорий, в которых есть новые статьи
    last_week = timezone.now() - timedelta(days=7)
    cats = list(Post.objects.filter(
        date_pub__gte=last_week,
    ).values_list('post_cat', flat=True).distinct())

    # Отправляем письма
    counter_mails = 0
    connection = None
    for cat in cats:
        try:
            connection = mail.get_connection()
            connection.open()
        except Exception as e:
            print(e)
        else:
            # Получаем список подписчиков на категорию
            subscribers = list(CatSubscribers.objects.filter(
                category=cat,
            ).values_list('subscriber', flat=True))

            if subscribers:
                # Подготавливаем и отправляем письмо
                for subscriber in subscribers:
                    receiver = User.objects.get(pk=subscriber)
                    category = Category.objects.get(pk=cat)
                    title_list = list(Post.objects.filter(
                        post_cat=cat,
                        date_pub__gte=last_week,
                    ).values_list('pk', 'name'))

                    if not receiver.first_name:
                        firstname = receiver.username
                    else:
                        firstname = receiver.first_name

                    print(f'Sending Email for {firstname} ...')

                    html_content = render_to_string(
                        'email/weekly_notify.html',
                        {
                            'name': firstname,
                            'category': category.name,
                            'titles': title_list,
                            'link': link,
                            'site_name': site.name,
                        }
                    )

                    message = mail.EmailMultiAlternatives(
                        subject=f'{firstname}, '
                                f'недельный дайджест статей в категории '
                                f'"{category.name}"',
                        from_email=os.getenv('EMAIL'),
                        to=[receiver.email],
                        connection=connection,
                    )
                    message.attach_alternative(html_content, 'text/html')
                    message.send()
                    counter_mails += 1

                    print(f'Email for {firstname} is sent')

        finally:
            connection.close()
    print(f'{counter_mails} Emails is sent')
