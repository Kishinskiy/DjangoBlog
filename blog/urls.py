from django.urls import path

from .views import (ArticleCreateView, ArticleDetailView, ArticleListView,
                    CategoryListView, get_stats, search_articles)

urlpatterns = [
    path('', ArticleListView.as_view(), name='index'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category_list'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('search/', search_articles, name='search'),
    path('stats/', get_stats, name='stats'),
]
