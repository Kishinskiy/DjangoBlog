from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from .models import Article, Category


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_articles'] = Article.objects.filter(
            is_published=True).count()
        context['total_categories'] = Category.objects.count()
        return context

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            if self.request.GET.get('page'):
                return ['blog/article_cards.html']
            return ['blog/article_list.html']
        return ['blog/index.html']


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related('author', 'category')

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['blog/article_detail.html']
        return ['blog/article_detail.html']


class CategoryListView(ListView):
    model = Article
    template_name = 'blog/category_list.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Article.objects.filter(
            category=self.category,
            is_published=True
        ).select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['blog/category_list.html']
        return ['blog/category_list.html']


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'blog/create.html'
    fields = ['title', 'slug', 'content',
              'excerpt', 'category', 'featured_image']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def search_articles(request):
    query = request.GET.get('q', '')
    articles = []

    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query),
            is_published=True
        ).select_related('author', 'category')[:10]

    context = {
        'articles': articles,
        'query': query,
        'total_results': len(articles)
    }

    if request.headers.get('HX-Request'):
        return render(request, 'blog/search_results.html', context)
    return render(request, 'blog/search.html', context)


def get_stats(request):
    """Возвращает статистику блога для HTMX обновления"""
    total_articles = Article.objects.filter(is_published=True).count()
    total_categories = Category.objects.count()

    context = {
        'total_articles': total_articles,
        'total_categories': total_categories
    }

    return render(request, 'blog/stats.html', context)
