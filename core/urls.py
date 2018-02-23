from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.list_category, name='list_category'),
    path('<int:category_pk>/', views.list_article, name='list_article'),
    path('<int:category_pk>/create/', views.create_article, name='create_article'),
    path('<int:category_pk>/<int:pk>/', views.detail_article, name='detail_article'),
    path('<int:category_pk>/<int:pk>/update/', views.update_article, name='update_article'),
    path('like/article/<int:pk>/', views.like_article, name='like_article'),
]
