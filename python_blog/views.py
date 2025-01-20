from django.shortcuts import render

from django.urls import reverse
from .models import Post, Category, Tag

# Импортируем Count
from django.db.models import Count, Q
from django.contrib.messages import constants as messages
from django.contrib import messages


CATEGORIES = [
    {"slug": "python", "name": "Python"},
    {"slug": "django", "name": "Django"},
    {"slug": "postgresql", "name": "PostgreSQL"},
    {"slug": "docker", "name": "Docker"},
    {"slug": "linux", "name": "Linux"},
]

MESSAGE_TAGS = {
    messages.DEBUG: "primary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}


def main(request):
    catalog_categories_url = reverse("blog:categories")
    catalog_tags_url = reverse("blog:tags")

    context = {
        "title": "Главная страница",
        "text": "Текст главной страницы",
        "user_status": "moderator",
    }
    return render(request, "main.html", context)


def about(request):
    context = {
        "title": "О компании",
        "text": "Мы - команда профессионалов в области веб-разработки",
    }
    return render(request, "about.html", context)


def catalog_posts(request):
    # Базовый QuerySet с оптимизацией запросов
    posts = Post.objects.select_related('category', 'author').prefetch_related('tags').all()
    
    # Получаем параметры поиска
    search_query = request.GET.get('search_query', '')
    
    if search_query:
        # Инициализируем пустой Q-объект
        search_conditions = Q()
        
        # Собираем условия поиска на основе выбранных критериев
        search_mapping = {
            'search_content': Q(content__icontains=search_query),
            'search_title': Q(title__icontains=search_query),
            'search_tags': Q(tags__name__icontains=search_query),
            'search_category': Q(category__name__icontains=search_query),
            'search_slug': Q(slug__icontains=search_query),
        }
        
        # Проверяем каждый критерий поиска и добавляем его в условия
        for param, condition in search_mapping.items():
            if request.GET.get(param) == '1':
                search_conditions |= condition
        
        # Применяем фильтрацию если есть условия
        if search_conditions:
            posts = posts.filter(search_conditions).distinct()
    
    # Настройки сортировки
    sort_mapping = {
        'created_date': '-created_at',
        'view_count': '-views',
        'update_date': '-updated_at',
    }
    
    # Получаем параметр сортировки или используем значение по умолчанию
    sort_by = request.GET.get('sort_by', 'created_date')
    sort_field = sort_mapping.get(sort_by, '-created_at')
    
    # Применяем сортировку
    posts = posts.order_by(sort_field)
    
    # Добавляем информационное сообщение при поиске
    if search_query:
        search_criteria = []
        criteria_mapping = {
            'search_content': 'контенте',
            'search_title': 'заголовках',
            'search_tags': 'тегах',
            'search_category': 'категориях',
            'search_slug': 'slug',
        }
        
        for param, description in criteria_mapping.items():
            if request.GET.get(param) == '1':
                search_criteria.append(description)
        
        if search_criteria:
            criteria_str = ', '.join(search_criteria)
            messages.info(
                request, 
                f'Результаты поиска "{search_query}" в {criteria_str}. '
                f'Найдено постов: {posts.count()}'
            )
    
    context = {
        'title': 'Блог',
        'posts': posts,
    }
    
    return render(request, 'blog.html', context)



def post_detail(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    context = {"title": post.title, "post": post}
    return render(request, "post_detail.html", context)


def catalog_categories(request):
    categories = Category.objects.all()
    context = {"categories": categories, "title": "Категории блога"}
    return render(request, "catalog_categories.html", context)


def category_detail(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    posts = category.posts.all()
    context = {
        "category": category,
        "posts": posts,
        "title": f"Категория: {category.name}",
        "active_menu": "categories",  # Добавляем флаг активного меню
    }
    return render(request, "category_detail.html", context)


def catalog_tags(request):
    # Получаем все теги и аннотируем их количеством постов
    tags = Tag.objects.annotate(posts_count=Count("posts")).order_by("-posts_count")

    context = {"tags": tags, "title": "Теги блога", "active_menu": "tags"}
    return render(request, "catalog_tags.html", context)


def tag_detail(request, tag_slug):
    # Получаем все посты конкретного тега через многие-ко-многим
    tag = Tag.objects.get(slug=tag_slug)
    posts = tag.posts.all()

    context = {
        "tag": tag,
        "posts": posts,
        "title": f"Тег: {tag.name}",
        "active_menu": "tags",  # Добавляем флаг активного меню
    }

    return render(request, "tag_detail.html", context)
