from django.contrib import admin
from django.urls import path
from python_blog.views import main
"""
Конверторы путей Django:
str - строки, любые символы кроме слэша '/' (по умолчанию)
int - положительные целые числа включая 0
slug - ASCII буквы/цифры, дефисы и подчеркивания
uuid - уникальные идентификаторы UUID
path - строки, включая слэши '/'

Пример использования:
path('articles/<int:year>/', views.year_archive)
path('blog/<slug:post_slug>/', views.post_detail)

"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:name>/', main)
]
