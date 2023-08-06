from django.db import models
from djangoarticle.models import ArticleModelScheme
from django.contrib.auth.models import User


class ArticleBookmarkModelScheme(models.Model):
    article    = models.ForeignKey(ArticleModelScheme, on_delete=models.CASCADE)
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"
        ordering = ["-pk"]