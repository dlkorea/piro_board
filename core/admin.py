from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from .models import Category, Article, Comment


class ArticleAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = 'content'


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
