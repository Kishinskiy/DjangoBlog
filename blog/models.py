import os

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True,
                            verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

def article_upload_path(instance, filename):
    return os.path.join('articles', str(instance.author.username), filename)

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержание')
    excerpt = models.TextField(
        max_length=300, blank=True, verbose_name='Краткое описание')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name='Категория')
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(
        default=True, verbose_name='Опубликовано')
    featured_image = models.ImageField(
        upload_to=article_upload_path,
        blank=True,
        null=True,
        verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']
