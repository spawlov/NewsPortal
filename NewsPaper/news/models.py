from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    author_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    author_rate = models.SmallIntegerField(
        default=0,
    )

    def update_rate(self):
        post_rate = self.post_set.all().aggregate(
            post_rating=Sum('content_rate')
        )
        p_rate = 0
        p_rate += post_rate.get('post_rating')

        comm_rate = self.author_user.comment_set.all().aggregate(
            comment_rating=Sum('comment_rate')
        )
        c_rate = 0
        c_rate += comm_rate.get('comment_rating')

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
    )

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
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    type_cat = models.CharField(
        max_length=3,
        choices=CHOICE_CAT,
        default=ARTICLE,
        verbose_name='Тип контента',
    )
    date_pub = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    post_cat = models.ManyToManyField(
        Category,
        through='PostCategory',
    )
    name = models.CharField(
        max_length=128,
        verbose_name='Название',
    )
    content = models.TextField(
        verbose_name='Контент',
    )
    content_rate = models.SmallIntegerField(
        default=0,
        verbose_name='Рейтинг',
    )

    def like(self):
        self.content_rate += 1
        self.save()

    def dislike(self):
        self.content_rate -= 1
        self.save()

    def preview(self):
        return f'{self.content[0:127]}...'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
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
