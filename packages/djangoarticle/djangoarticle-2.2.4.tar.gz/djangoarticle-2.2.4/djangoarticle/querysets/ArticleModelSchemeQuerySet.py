from django.db import models 


class ArticleModelSchemeQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='publish')

    def status(self, status, author):
        return self.filter(status=status, author=author)

    def promoted(self):
        return self.published().filter(is_promote=True)

    def trending(self):
        return self.published().filter(is_trend=True)

    def author(self, username):
        return self.published().filter(author__username=username)

    def promotional(self):
        return self.published().filter(is_promotional=True)

    def opinion(self):
        return self.published().filter(is_opinion=True)

    def promoted_only(self):
        return self.published().filter(is_promote=True, is_trend=False, is_promotional=False, is_opinion=False)

    def trending_only(self):
        return self.published().filter(is_trend=True, is_promote=False, is_promotional=False, is_opinion=False)

    def promotional_only(self):
        return self.published().filter(is_promotional=True, is_trend=False, is_promote=False, is_opinion=False)

    def administrator_or_author(self, user):
        if user.groups.filter(name="Administrator").exists():
            return self.published()
        return self.author(user)

    def bookmarks(self, user):
        return self.published().filter(bookmarks__username=user.username)