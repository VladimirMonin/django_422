# python_blog\urls.py Django APP python_blog
from django.contrib import admin
from django.urls import path
from python_blog.views import catalog_posts, post_detail, catalog_categories, category_detail, catalog_tags, tag_detail,


urlpatterns = [
    path('', catalog_posts),
    path('<slug:slug>/', post_detail), # /posts/osnovy-python/
   
   # Категории
    path('categories/', catalog_categories),
    path('categories/<slug:slug>/', category_detail),
   
   # Теги
    path('tags/', catalog_tags),
    path('tags/<slug:slug>/', tag_detail),

]
