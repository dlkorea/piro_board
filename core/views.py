from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.views.generic import (
    View,
    DetailView,
    ListView,
)
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.http import JsonResponse

from .models import Category, Article
from .forms import ArticleForm


# def list_category(request):
#     category_list = Category.objects.all()
#     ctx = {
#         'category_list': category_list,
#     }
#     return render(request, 'core/category_list.html', ctx)


class CategoryListView(ListView):
    model = Category
    template_name = 'core/category_list.html'


list_category = CategoryListView.as_view()


def list_article(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    article_list = Article.objects.filter(category=category)

    paginate_by = 15
    last_page = article_list.count() // paginate_by + 1

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    page = max(page, 1)
    page = min(page, last_page)

    min_page = page - 2
    max_page = page + 2
    if min_page < 1:
        min_page = 1
        max_page = min(5, last_page)
    elif max_page > last_page:
        min_page = max(1, last_page - 4)
        max_page = last_page

    page_list = [i for i in range(min_page, max_page + 1)]
    ctx = {
        'category': category,
        'article_list': article_list[paginate_by * (page-1):paginate_by * page],
        'page': page,
        'page_list': page_list,
        'is_first_page': page == 1,
        'is_last_page': page == last_page,
    }
    return render(request, 'core/article_list.html', ctx)


# @login_required
# def detail_article(request, category_pk, article_pk):
#     article = get_object_or_404(Article, pk=article_pk)
#     ctx = {
#         'article': article,
#         'liked': article.is_liked_by(request.user),
#     }
#     return render(request, 'core/article_detail.html', ctx)


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'core/article_detail.html'


detail_article = ArticleDetailView.as_view()


# @require_POST
# @login_required
# def like_article(request, pk):
#     article = get_object_or_404(Article, pk=pk)
#     ctx = {
#         'article': article,
#         'liked': article.toggle_like(request.user),
#     }
#     return render(request, 'core/article_like_button.html', ctx)


class LikeView(LoginRequiredMixin, SingleObjectMixin, View):
    """
    core.models.LikeMixinModel 과 연동.
    """
    model = None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {
            'liked': self.object.toggle_like(request.user),
            'like_count': self.object.count_like(),
        }
        return JsonResponse(data)


like_article = LikeView.as_view(model=Article)


@login_required
def create_article(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    form = ArticleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        article = form.save(commit=False)
        article.category = category
        article.author = request.user
        article.save()
        return redirect(reverse('core:detail_article', kwargs={
            'category_pk': category.pk,
            'pk': article.pk,
        }))
    ctx = {
        'category': category,
        'form': form,
    }
    return render(request, 'core/article_create.html', ctx)


@login_required
def update_article(request, category_pk, pk):
    category = get_object_or_404(Category, pk=category_pk)
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(request.POST or None, instance=article)
    if request.method == 'POST' and form.is_valid():
        article = form.save()
        return redirect(reverse('core:detail_article', kwargs={
            'category_pk': category.pk,
            'pk': article.pk,
        }))
    ctx = {
        'category': category,
        'form': form,
    }
    return render(request, 'core/article_create.html', ctx)
