from django.shortcuts import render, get_object_or_404

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

    ctx = {
        'category': category,
        'article_list': article_list[paginate_by * (page-1):paginate_by * page],
        'page': page,
        'page_list': page_list,
        'is_first_page': page == 1,
        'is_last_page': page == last_page,
    }
    return render(request, 'core/article_list.html', ctx)
