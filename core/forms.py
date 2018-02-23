from django import forms

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('category', 'author', 'liker_set', )
        widgets = {
            'content': SummernoteWidget(),
        }
