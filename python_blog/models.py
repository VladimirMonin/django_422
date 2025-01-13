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
    tags = models.ManyToManyField("Tag", related_name="posts", verbose_name="Теги")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Слаг")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("blog:tag_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]
    



class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Слаг")
    description = models.TextField(
        blank=True, null=True, default="Без описания", verbose_name="Описание"
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("blog:category_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


#PRACTICE Практика с многие ко многим и Shell plus
"""
0. Запуск shell plus с print sql
python manage.py shell_plus --print-sql

1. Создадим ещё пару постов

post1 = Post.objects.create(title="Django ORM", content="Изучаем Django ORM")
post2 = Post.objects.create(title="Python Basic", content="Основы Python")

# Создаем пару тегов
tag1 = Tag.objects.create(name="Python")
tag2 = Tag.objects.create(name="Django")

# Добавляем теги к постам
post1.tags.add(tag1, tag2)  # Первому посту добавляем оба тега
post2.tags.add(tag1)  # Второму посту добавляем только тег Python

# Получим пост со всеми тегами
post_1 = Post.objects.get(id=1)

# Получим теги
post_1.tags - Получим manager для связи многие ко многим
Мы можем вызвать его методы и получить все теги, связанные с этим постом.
tags = post_1.tags.all() - кверисет

# Посчитаем количество тегов у поста
post_1.tags.count() - 2

# Получим теги в которых есть py в имени
post_1.tags.filter(name__icontains="PY")

name - поле модели Tag
__icontains - фильтр по подстроке

# Посчитаем количество постов у тега tag1

posts_count = tag1.posts.count()

# Получим все посты у которых есть тег tag1
post_with_tag1 = tag1.posts.all()

# Удалим тег tag2 у post1
post1.tags.remove(tag2)

# Обновим данные в переменной post_1
post_1.refresh_from_db()
"""