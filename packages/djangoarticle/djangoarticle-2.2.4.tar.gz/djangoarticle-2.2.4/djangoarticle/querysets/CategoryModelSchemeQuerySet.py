from django.db import models 


class CategoryModelSchemeQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='publish')

    def status(self, status, author):
        return self.filter(status=status, author=author)

    def author(self, username):
        return self.published().filter(author=username)

    def administrator_or_author(self, user):
        if user.groups.filter(name="Administrator").exists():
            return self.published()
        return self.author(user)