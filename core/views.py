from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Category, Article


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
    # page_list = []
    # for i in range(1, last_page+1):
    #     if
    #     page_list.append(i)

    ctx = {
        'category': category,
        'article_list': article_list[paginate_by * (page-1):paginate_by * page],
        'page': page,
        'page_list': page_list,
        'is_first_page': page == 1,
        'is_last_page': page == last_page,
    }
    return render(request, 'core/article_list.html', ctx)


@login_required
def detail_article(request, category_pk, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    ctx = {
        'article': article,
        'liked': article.is_liked_by(request.user),
    }
    return render(request, 'core/article_detail.html', ctx)


@require_POST
@login_required
def like_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    ctx = {
        'article': article,
        'liked': article.toggle_like(request.user),
    }
    return render(request, 'core/article_like_button.html', ctx)
