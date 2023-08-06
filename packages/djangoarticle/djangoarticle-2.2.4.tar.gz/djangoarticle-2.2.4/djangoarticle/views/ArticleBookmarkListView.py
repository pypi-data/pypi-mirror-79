from django.views.generic import ListView
from django.db.models import Q
from djangoarticle.models import ArticleModelScheme
from django.contrib.auth.mixins import LoginRequiredMixin


class ArticleBookmarkListView(LoginRequiredMixin, ListView):
    template_name = "djangoadmin/djangoarticle/article_list_dashboard.html"
    context_object_name = "article_filter"
    paginate_by = 10

    def get_queryset(self):
        article_filter = ArticleModelScheme.objects.bookmarks(self.request.user)
        query = self.request.GET.get("query")
        if query:
            article_match = ArticleModelScheme.objects.bookmarks(self.request.user).filter(Q(title__icontains=query))
            if article_match:
                return article_match
            else:
                return list()
        else:
            return article_filter
        return article_filter