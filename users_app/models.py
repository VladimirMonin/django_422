# В будущем для подисок можно сделать 
# Таблицу с описанием подписок
# UserSubscriptionHistory связана с User через ForeignKey - Для того чтобы знать какие подписки были у пользователя в прошлом


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='users/avatars/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    github_id = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name='GitHub ID'
    )
    vk_id = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name='VK ID'
    )
    telegram_id = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name='Telegram ID'
    )
    birth_date = models.DateField(
        blank=True, 
        null=True,
        verbose_name='Дата рождения'
    )
    bio = models.TextField(
        max_length=1000, 
        blank=True,
        verbose_name='О себе'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
