from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .form import PostingForm
from .models import Post, PostCategory, Comment, Category, CatSubscribers, Author


class PostCategoryInLine(admin.TabularInline):
    model = PostCategory
    fk_name = 'post'
    extra = 1


class PostAdmin(TranslationAdmin):
    model = Post
    form = PostingForm
    list_display = (
        'name', 'author_post', 'date_pub', 'content_rate',
    )
    ordering = ['-date_pub']
    list_filter = ['date_pub', 'type_cat', 'author_post', ]
    search_fields = ['name']
    readonly_fields = ['date_pub', 'content_rate', ]
    fieldsets = [
        (_('Автор'), {'fields': ['author_post', ]}),
        (_('Тип'), {'fields': ['type_cat', ]}),
        (_('Содержание'), {'fields': ['name', 'content_image', 'content', ]}),
        (_('Информация о посте'), {'fields': ['date_pub', 'content_rate', ]}),
    ]
    inlines = [PostCategoryInLine]


class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        'comments', 'post', 'user', 'date_comment', 'comment_rate',
    )
    ordering = ['-date_comment']
    list_filter = ['date_comment', 'user']
    search_fields = ['comment']
    # readonly_fields = ['user', 'post', 'date_comment', 'comment_rate', ]
    #
    # fieldsets = [
    #     ('Комментарий', {'fields': ['comment', ]}),
    #     ('Информация о комментарии', {
    #         'fields': ['user', 'date_comment', 'post', 'comment_rate', ]
    #     }),
    # ]


class CategoryAdmin(TranslationAdmin):
    model = Category
    list_display = ['name', 'name_ru', 'name_en']


class AuthorAdmin(admin.ModelAdmin):
    model = Author
    list_display = ['author_user', 'language', 'timezone', 'author_rate']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(CatSubscribers)
