from django.contrib import admin

from .form import PostingForm
from .models import Post, PostCategory, Comment, Category, CatSubscribers


class PostCategoryInLine(admin.TabularInline):
    model = PostCategory
    fk_name = 'post'
    extra = 1


class PostAdmin(admin.ModelAdmin):
    form = PostingForm
    list_display = (
        'name', 'author_post', 'date_pub', 'content_rate',
    )
    ordering = ['-date_pub']
    list_filter = ['date_pub', 'type_cat', 'author_post', ]
    search_fields = ['name']
    readonly_fields = ['date_pub', 'content_rate', ]
    fieldsets = [
        ('Автор', {'fields': ['author_post', ]}),
        ('Контент', {'fields': ['type_cat', ]}),
        ('Содержание', {'fields': ['name', 'content', ]}),
        ('Информация о посте', {'fields': ['date_pub', 'content_rate', ]}),
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


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(CatSubscribers)

