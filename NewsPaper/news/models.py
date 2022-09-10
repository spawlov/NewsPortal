from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy


class Author(models.Model):
    author_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Имя',
    )
    author_rate = models.SmallIntegerField(
        default=0,
        verbose_name='Рейтинг',
    )

    def update_rate(self):
        """Расчет рейтинга автора"""
        post_rating = 0
        post_rate = self.post_set.all().aggregate(
            post_rating=Sum('content_rate')
        )
        if post_rate.get('post_rating'):
            post_rating = post_rate.get('post_rating')
        p_rate = 0
        p_rate += post_rating

        comment_rating = 0
        comm_rate = self.author_user.comment_set.all().aggregate(
            comment_rating=Sum('comment_rate')
        )
        if comm_rate.get('comment_rating'):
            comment_rating = comm_rate.get('comment_rating')
        c_rate = 0
        c_rate += comment_rating
        print(c_rate)
        self.author_rate = p_rate * 3 + c_rate
        self.save()

    def __str__(self):
        return self.author_user.username

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Имя категории',
    )
    subscribers = models.ManyToManyField(
        User,
        through='CatSubscribers',
        blank=True,
        verbose_name='Подписчик',
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        key = make_template_fragment_key('navbar')
        cache.delete(key)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author_post = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    ARTICLE = 'ART'
    NEWS = 'NWS'
    CHOICE_CAT = [
        (ARTICLE, _('Статья')),
        (NEWS, _('Новость')),
    ]
    type_cat = models.CharField(
        max_length=3,
        choices=CHOICE_CAT,
        default=ARTICLE,
        verbose_name=_('Тип контента'),
    )

    date_pub = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата публикации'),
    )

    post_cat = models.ManyToManyField(
        Category,
        through='PostCategory',
        verbose_name=_('Категория'),
    )

    name = models.CharField(
        max_length=128,
        verbose_name=_('Название'),
    )

    content = models.TextField(
        verbose_name=_('Контент'),
    )

    content_rate = models.SmallIntegerField(
        default=0,
        verbose_name=_('Рейтинг'),
    )

    content_image = models.ImageField(
        upload_to='images',
        verbose_name=_('Изображение'),
        default='no_image.jpg',
    )

    def like(self):
        self.content_rate += 1
        self.save()

    def dislike(self):
        self.content_rate -= 1
        self.save()

    def preview(self):
        return f'{self.content[0:127]}...'

    def get_absolute_url(self):
        return reverse('news:detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-id-{self.pk}')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
    )
    cat = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )

    def __str__(self):
        return self.cat.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    comment = models.TextField(
        verbose_name='Текст комментария',
    )
    date_comment = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария',
    )
    comment_rate = models.SmallIntegerField(
        default=0,
        verbose_name='Рейтинг',
    )

    @property
    def comments(self):
        if len(self.comment) > 32:
            return f'{self.comment[:31]}...'
        else:
            return self.comment

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()

    def __str__(self):
        return self.comments

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class CatSubscribers(models.Model):
    subscriber = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )

    def __str__(self):
        return f'' \
               f'{self.subscriber.username} ({self.subscriber.email}), ' \
               f'категория: {self.category}'

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
