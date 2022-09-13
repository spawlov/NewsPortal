import os

import requests
from bs4 import BeautifulSoup
import shutil

from django.utils import timezone

from .models import Post


def article_parser(parsing_url: str) -> tuple:
    """Парсинг последней статьи с сайта https://naked-science.ru/"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'
    }
    site_to_parse = requests.get(parsing_url, headers=headers)
    resp = site_to_parse.status_code
    if resp == 200:
        link_last = BeautifulSoup(
            site_to_parse.text, 'lxml'
        ).find(
            'div', class_='news-item-title'
        ).find(
            'a', class_='animate-custom'
        ).get('href')

        news_to_parse = requests.get(link_last, headers=headers)
        news_page = BeautifulSoup(news_to_parse.text, 'lxml')
        title = news_page.find('div', class_='post-title').find('h1').text
        title = title.strip()
        date_pub = news_page.find('div', class_='meta-item').find(
            'span', class_='echo_date'
        ).get('data-published')
        image = news_page.find('div', class_='post-image-inner').find(
            'a', class_='lightbox'
        ).get('href')

        image_name = image.split('/')[-1]
        full_image_name = f'images/{timezone.now().strftime("%Y/%m/%d")}/{image_name}'

        r = requests.get(image, stream=True)
        exists = Post.objects.filter(name_ru__icontains=title).exists()
        if all([r.status_code == 200, not exists]):
            if not os.path.exists(f'images/{timezone.now().strftime("%Y/%m/%d")}'):
                os.makedirs(f'images/{timezone.now().strftime("%Y/%m/%d")}')

            with open(full_image_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

        post_p = []

        body_lead = news_page.find('div', class_='post-lead').find('p').text
        post_p.append(body_lead.strip())

        body = news_page.find('div', class_='body')
        pre_p = body.find_all('p')

        for p in pre_p:
            post_p.append(p.text.strip())

        content = ''
        for par in post_p:
            content += f'<p>{par}</p>'

        return resp, title, content, full_image_name, date_pub
    else:
        return resp, None, None, None, None
