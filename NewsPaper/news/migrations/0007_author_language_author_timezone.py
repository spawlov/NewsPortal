# Generated by Django 4.1 on 2022-09-12 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_post_content_en_post_content_ru_post_name_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='language',
            field=models.CharField(default=None, max_length=10, null=True, verbose_name='Язык'),
        ),
        migrations.AddField(
            model_name='author',
            name='timezone',
            field=models.CharField(default=None, max_length=32, null=True, verbose_name='Часовой пояс'),
        ),
    ]