from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Post, Category, Tag
from django.db.models import Count, Q, F
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
    posts = (
        Post.objects.select_related("category", "author").prefetch_related("tags").all()
    )

    # Получаем строку поиска
    search_query = request.GET.get("search_query", "")

    if search_query:
        # Создаем пустой Q объект
        q_object = Q()

        # Добавляем условия поиска если включены соответствующие чекбоксы
        if request.GET.get("search_content") == "1":
            q_object |= Q(content__icontains=search_query)

        if request.GET.get("search_title") == "1":
            q_object |= Q(title__icontains=search_query)

        if request.GET.get("search_tags") == "1":
            q_object |= Q(tags__name__icontains=search_query)

        if request.GET.get("search_category") == "1":
            q_object |= Q(category__name__icontains=search_query)

        if request.GET.get("search_slug") == "1":
            q_object |= Q(slug__icontains=search_query)

        # Применяем фильтрацию если есть хотя бы одно условие
        if q_object:
            posts = posts.filter(q_object).distinct()

    # Сортировка результатов
    sort_by = request.GET.get("sort_by", "created_date")

    if sort_by == "view_count":
        posts = posts.order_by("-views")
    elif sort_by == "update_date":
        posts = posts.order_by("-updated_at")
    else:
        posts = posts.order_by("-created_at")

    # Создаем объект пагинатора, 2 поста на страницу
    paginator = Paginator(posts, 2)

    # Получаем номер текущей страницы
    page_number = request.GET.get("page", 1)

    # Получаем объект страницы
    page_obj = paginator.get_page(page_number)

    context = {
        "title": "Блог",
        "posts": page_obj,  # Теперь передаем страницу вместо queryset
        "page_obj": page_obj,  # Добавляем объект страницы в контекст
    }

    return render(request, "blog.html", context)


def post_detail(request, post_slug):
    """
    Вью детального отображения поста.
    Увеличивает количество просмотров поста через F-объект.
    """

    # Получаем пост

    post = (
        Post.objects.select_related("category", "author")
        .prefetch_related("tags")
        .get(slug=post_slug)
    )

    # Добываем сессию
    session = request.session

    # Формируем ключ для сессии
    key = f"viewed_posts_{post.id}"

    # Если пост не был просмотрен
    if key not in session:
        # Увеличиваем количество просмотров
        Post.objects.filter(id=post.id).update(views=F("views") + 1)
        # Записываем в сессию, что пост был просмотрен
        session[key] = True
        post.refresh_from_db()  # Обновляем объект

    context = {"title": post.title, "post": post}
    return render(request, "post_detail.html", context)


def catalog_categories(request):
    categories = Category.objects.all()
    context = {"categories": categories, "title": "Категории блога"}
    return render(request, "catalog_categories.html", context)


def category_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        if name:
            category = Category.objects.create(
                name=name, description=description or "Без описания"
            )
            messages.success(request, f'Категория "{category.name}" успешно создана!')
            return redirect("blog:categories")

    return render(request, "category_create.html", {"title": "Создание категории"})


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
