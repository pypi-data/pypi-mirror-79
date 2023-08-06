from django.db import models
from djangoarticle.querysets import CategoryModelSchemeQuerySet


class CategoryModelSchemeManager(models.Manager):
    def get_queryset(self):
        return CategoryModelSchemeQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def status(self, status, author):
        return self.get_queryset().status(status, author)

    def author(self, username):
        return self.get_queryset().author(username)

    def administrator_or_author(self, user):
        return self.get_queryset().administrator_or_author(user)