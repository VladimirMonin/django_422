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


#PRACTICE Практика с лукапами и Shell plus

# Запуск shell plus
python .\manage.py shell_plus --print-sql

# Все посты определенной категории
Post.objects.filter(category__name="Python")

# Все посты с определенным тегом
Post.objects.filter(tags__name="Django")

# Посты у которых автор имеет определенный email (регистрозависимое вхождение)
Post.objects.filter(author__email__contains="admin")

# Посты за 2024 год
Post.objects.filter(created_at__year=2024)

# Поищем посты РАНЕЕ чем 2025 год
Post.objects.filter(created_at__lt=datetime(2025, 1, 1))

# Посты с годом создания меньше 2025
Post.objects.filter(created_at__year__lt=2025)

# Посты с годом создания больше 2020
Post.objects.filter(created_at__year__gt=2020)

# Посты с годом создания между 2020 и 2024
Post.objects.filter(created_at__year__range=(2020, 2024))


# Посты за последний месяц
from datetime import datetime, timedelta
month_ago = datetime.now() - timedelta(days=30)
Post.objects.filter(created_at__gte=month_ago)

# Посты обновленные сегодня
from django.utils import timezone
today = timezone.now().date()
Post.objects.filter(updated_at__date=today)

# Поиск постов по части заголовка
Post.objects.filter(title__icontains="python")

# Поиск категорий по части названия
Category.objects.filter(name__icontains="прог")

# Поиск тегов начинающихся с определенных букв
Tag.objects.filter(name__istartswith="py")

# Точное совпадение заголовка
Post.objects.filter(title__exact="Django ORM")

# Регистронезависимое точное совпадение
Post.objects.filter(title__iexact="django orm")

# Точное совпадение слага
Post.objects.get(slug__exact="django-orm")

# Посты с количеством просмотров больше 100 и тегом "Python"
Post.objects.filter(views__gt=100, tags__name="Python")

# Посты без категории
Post.objects.filter(category__isnull=True)

# Посты в определенном диапазоне просмотров
Post.objects.filter(views__range=(10, 100))

# Топ-5 самых просматриваемых постов
Post.objects.order_by('-views')[:3]


# Последние посты определенной категории
Post.objects.filter(category__name="Python").order_by('-created_at')[:10]

# Посты с более чем одним тегом
# Импорт Count
from django.db.models import Count
Post.objects.annotate(tags_count=Count('tags')).filter(tags_count__gt=0)
