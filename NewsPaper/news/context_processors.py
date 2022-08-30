from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth

from .models import Category, Post


def navigate_context(request):
    # Контекст для блоков повторяющихся на всех страницах
    category = Category.objects.all()
    archives = Post.objects.annotate(
        year=ExtractYear('date_pub'),
        month=ExtractMonth('date_pub')
    ).values('year', 'month').annotate(total=Count('id'))

    context = {
        'category': category,
        'archives': archives,
    }

    return context
