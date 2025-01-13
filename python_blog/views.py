from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from .models import Post, Category, Tag
# Импортируем Count
from django.db.models import Count

CATEGORIES = [
    {"slug": "python", "name": "Python"},
    {"slug": "django", "name": "Django"},
    {"slug": "postgresql", "name": "PostgreSQL"},
    {"slug": "docker", "name": "Docker"},
    {"slug": "linux", "name": "Linux"},
]


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
    posts = Post.objects.all()
    context = {"title": "Блог", "posts": posts}
    return render(request, "blog.html", context)


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
        "active_menu": "categories"  # Добавляем флаг активного меню
    }
    return render(request, "category_detail.html", context)



def catalog_tags(request):
    # Получаем все теги и аннотируем их количеством постов
    tags = Tag.objects.annotate(posts_count=Count('posts')).order_by('-posts_count')
    
    context = {
        'tags': tags,
        'title': 'Теги блога',
        'active_menu': 'tags'
    }
    return render(request, 'catalog_tags.html', context)



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
