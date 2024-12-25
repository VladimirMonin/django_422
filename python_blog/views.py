from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from .blog_data import dataset
from .models import Post, Category


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
    # Получаем все опубликованные посты
    posts = [post for post in dataset if post['is_published']]
    context = {
        'title': 'Блог',
        'posts': posts
    }
    return render(request, 'blog.html', context)


def post_detail(request, post_slug):
    # Находим нужный пост по slug
    post = next((post for post in dataset if post['slug'] == post_slug), None)
    
    context = {
        'title': post['title'],
        'post': post
    }
    return render(request, 'post_detail.html', context)

def catalog_categories(request):
    CATEGORIES = Category.objects.all()

    context = {
        "title": "Категории",
        "text": "Текст страницы с категориями",
        "categories": CATEGORIES,
    }
    return render(request, "catalog_categories.html", context)


def category_detail(request, category_slug):

    category = [cat for cat in CATEGORIES if cat["slug"] == category_slug][0]

    if category:
        name = category["name"]
    else:
        name = category_slug

    return HttpResponse(
        f"""
        <h1>Категория: {name}</h1>
        <p><a href="{reverse('blog:categories')}">Назад к категориям</a></p>
    """
    )


def catalog_tags(request):
    return HttpResponse("Каталог тегов")


def tag_detail(request, tag_slug):
    return HttpResponse(f"Страница тега {tag_slug}")
