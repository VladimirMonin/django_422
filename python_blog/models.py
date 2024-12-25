from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode
# Функция get_user_model() возвращает модель пользователя, которая используется по умолчанию в проекте.
from django.contrib.auth import get_user_model


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Заголовок")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Слаг", blank=True, null=True)
    content = models.TextField(verbose_name="Контент")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Автор", related_name="posts", default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    # категория - внешний ключ
    category = models.ForeignKey(
        "Category",  # Ссылка на модель Category
        on_delete=models.SET_NULL,  # При удалении категории, установить значение NULL
        blank=True,  # Не требуем в формах заполнения
        null=True,  # Разрешаем значение NULL в базе данных
        related_name="posts",  # Имя обратной связи
        default=None,  # По умолчанию значение NULL
        verbose_name="Категория",
    )
    tags = models.JSONField(null=True, blank=True, default=list, verbose_name="Теги") # default=list - по умолчанию пустой список

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """
        Метод возвращает абсолютный URL поста.
        В админке Django, при создании или редактировании поста, будет ссылка "Посмотреть на сайте." В шаблонах тоже удобно вызывать его.
        """
        return reverse("blog:post_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        """
        Служебный метод для сохранения объекта в базе данных.
        Мы расширяем его чтобы изменить логику сохранения объекта.
        """
        self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)
    
    class Meta:
        """
        Специальный вложенный класс для настроек модели.
        """
        ordering = ["-created_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Слаг")
    description = models.TextField(
        blank=True, null=True, default="Без описания", verbose_name="Описание"
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """
        Метод возвращает абсолютный URL категории.
        В админке Django, при создании или редактировании категории, будет ссылка "Посмотреть на сайте." В шаблонах тоже удобно вызывать его.
        """
        return reverse("blog:category_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        """
        Служебный метод для сохранения объекта в базе данных.
        Мы расширяем его чтобы изменить логику сохранения объекта.
        """
        self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)
    
    class Meta:
        """
        Специальный вложенный класс для настроек модели.
        """
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    


# PRACTICE - Работа с моделью Post
"""
1. Создать новый пост
post = Post(title="Django для чайников", content="Django очень лёгкий фреймворк, и у него пологая кривая входа...")
post.save()

INSERT INTO "python_blog_post" ("title", "content", "created_at", "updated_at", "category")
VALUES ('Django для чайников', 'Django очень лёгкий фреймворк, и у него пологая кривая входа...', '2024-12-23 17:30:53.551384', '2024-12-23 17:30:53.551410', NULL) RETURNING "python_blog_post"."id"
Execution time: 0.000827s [Database: default]


post_1 = post

post_2 = Post(title="Базы данных для продавцов котиков", content="Теперь вы сможете каждого котика сохранить в базе данных")

Django ORM ленива.
Все запросы по умолчанию выполняются в ленивом режиме.
Допустим при сохранении, запрос будет выполнен только при вызове метода save()

При чтении, запрос будет выполнен при обращении к результату запроса

2. Получить все посты

posts = Post.objects.all()
posts = <QuerySet [<Post: Post object (1)>, <Post: Post object (2)>]>

Что такое QuerySet?
QuerySet - это набор объектов, которые мы получили из базы данных.
Мы можем использовать QuerySet для фильтрации, сортировки, группировки и других операций над объектами.

post_1 = posts[0]
post_1

post_1.title
post_1.content

post_1.content = "Django не очень лёгкий фреймворк, но у него пологая кривая входа..."
post_1.save()

post_3 = Post(title="Тестовый пост", content="Тестовый пост")

# Делаем операцию удаления
post_3.delete()

3. Получить пост по id
post_1 = Post.objects.get(id=1) # id - поле модели id - это поле, которое автоматически генерируется Django
post_1 = Post.objects.get(pk=1) # pk - primary key - первичный ключ

4. Получим все посты и сортируем их по полю created_at от новых к старым
posts = Post.objects.all().order_by("-created_at")

5. Используя filter получим посты где категория NULL
posts = Post.objects.filter(category=None)
Применим к полученному querySet сортировку
posts = posts.order_by("-created_at")
"""

# PRACTICE - Работа с моделью Category

"""
0. Запускаем shell plus --print-sql
python manage.py shell_plus --print-sql

1. Создать новую категорию
category_1 = Category(name="Django", slug="django").save()
category_2 = Category(name="Python", slug="python").save()
category_3 = Category(name="Postgresql", slug="postgresql").save()
category_4 = Category(name="Docker", slug="docker").save()
category_5 = Category(name="Linux", slug="linux").save()


2. Получим все посты
posts = Post.objects.all()

3. Возьмем первый пост
post_1 = posts[0]

django_category = Category.objects.get(name="Django")

4. post_1 - хочу присвоить категорию django_category
post_1.category = django_category
post_1.save()

post_1 - это объект, который мы получили из базы данных
post_1.title - это поле title у объекта post_1
post_1.category - экземпляр объекта Category, который мы присвоили объекту post_1

post_1.category.name - Django

# Обратное связывание. Мы обозначили related_name="posts" в модели Post

# Получим все посты по объекту категории
category = Category.objects.get(name="Django")
django_posts = category.posts.all()

# Если бы не было related_name="posts"

category = Category.objects.get(name="Django")
django_posts = Post.objects.filter(category=category)
# или

django_posts = Post.objects.filter(category__name="Django")



######################## После обновления модели Category ########################

Пробуем создать категорию (Убедимся что кириллица не обрабатывается!!!!)

category_6 = Category(name="Linux Avrora").save()
category_7 = Category(name="Добрый добрый JS").save()

category_8 = Category(name="Постгра").save()
category_9 = Category(name="Оракл БД").save()


########## Создание суперпользователя ##########
"""
