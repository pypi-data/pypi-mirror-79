from django.db import models
from djangoarticle.querysets import ArticleModelSchemeQuerySet


class ArticleModelSchemeManager(models.Manager):
    def get_queryset(self):
        return ArticleModelSchemeQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def status(self, status, author):
        return self.get_queryset().status(status, author)

    def promoted(self):
        return self.get_queryset().promoted()

    def trending(self):
        return self.get_queryset().trending()

    def author(self, username):
        return self.get_queryset().author(username)

    def promotional(self):
        return self.get_queryset().promotional()

    def opinion(self):
        return self.get_queryset().opinion()

    def promoted_only(self):
        return self.get_queryset().promoted_only()

    def trending_only(self):
        return self.get_queryset().trending_only()

    def promotional_only(self):
        return self.get_queryset().promotional_only()

    def administrator_or_author(self, user):
        return self.get_queryset().administrator_or_author(user)

    def bookmarks(self, user):
        return self.get_queryset().bookmarks(user)