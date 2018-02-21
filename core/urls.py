from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('<int:category_pk>/', views.list_article, name='list_article'),
]
