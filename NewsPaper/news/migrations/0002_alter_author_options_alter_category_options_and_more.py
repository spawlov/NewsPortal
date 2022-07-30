# Generated by Django 4.0.6 on 2022-07-29 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AlterModelOptions(
            name='postcategory',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(verbose_name='Текст комментария'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_rate',
            field=models.SmallIntegerField(default=0, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_comment',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post', verbose_name='Пост'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='Контент'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content_rate',
            field=models.SmallIntegerField(default=0, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_pub',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='post',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='post',
            name='type_cat',
            field=models.CharField(choices=[('ART', 'Статья'), ('NWS', 'Новость')], default='ART', max_length=3, verbose_name='Тип контента'),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category', verbose_name='Категория'),
        ),
    ]
