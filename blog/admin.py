from django.contrib import admin

from .models import Article, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category',
                    'created_at', 'is_published')
    list_display_links = ('title',)
    search_fields = ('title', 'content', 'excerpt')
    list_filter = ('created_at', 'category', 'is_published', 'author')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
