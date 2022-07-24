from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rate = models.SmallIntegerField(default=0)

    def update_rate(self):
        pass


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)

    ARTICLE = 'ART'
    NEWS = 'NWS'
    CHOICE_CAT = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    type_cat = models.CharField(
        max_length=3, choices=CHOICE_CAT, default=ARTICLE
    )
    date_pub = models.DateTimeField(auto_now_add=True)
    post_cat = models.ManyToManyField(Category, through='PostCategory')
    name = models.CharField(max_length=128)
    content = models.TextField()
    content_rate = models.SmallIntegerField(default=0)

    def like(self):
        self.content_rate += 1
        self.save()

    def dislike(self):
        self.content_rate -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)
    comment_rate = models.SmallIntegerField(default=0)

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()
