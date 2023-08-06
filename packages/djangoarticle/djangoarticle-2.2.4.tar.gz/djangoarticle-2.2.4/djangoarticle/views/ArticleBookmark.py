from django.views.generic import View
from djangoarticle.models import ArticleModelScheme
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect


class ArticleBookmark(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(ArticleModelScheme, slug=kwargs['article_slug'])
        if article.bookmarks.filter(username=request.user.username):
            article.bookmarks.remove(request.user)
        else:
            article.bookmarks.add(request.user)
        return redirect("djangoarticle:article_list_view")