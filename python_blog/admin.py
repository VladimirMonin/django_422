from django.contrib import admin
from .models import Category, Post
# Регистрация 2 способами
"""
1. Регистрация с использованием функции register
2. Регистрация с использованием класса
"""

# 1. Регистрация с использованием функци и декоратора
admin.site.register(Category)

# 2. Регистрация с использованием класса
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']
    # Поля, которые будут отображаться в списке постов
    list_display = ["title", "created_at", "updated_at", "category"]


admin.site.register(Post, PostAdmin)
