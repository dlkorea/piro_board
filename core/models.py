from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class LikeMixinModel(models.Model):
    liker_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_%(class)s_set',
    )

    class Meta:
        abstract = True

    def count_like(self):
        return self.liker_set.count()

    def is_liked_by(self, user):
        return self.liker_set.filter(pk=user.pk).exists()

    def toggle_like(self, user):
        liked = self.is_liked_by(user)
        if liked:
            self.liker_set.remove(user)
        else:
            self.liker_set.add(user)
        return not liked


class Article(LikeMixinModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{pk}. {title}'.format(
            pk=self.pk,
            title=self.title,
        )


class Comment(LikeMixinModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
