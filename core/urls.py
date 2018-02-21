from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('<int:category_pk>/', views.list_article, name='list_article'),
    path('<int:category_pk>/<int:article_pk>/', views.detail_article, name='detail_article'),
    path('like/article/<int:pk>/', views.like_article, name='like_article'),
]
