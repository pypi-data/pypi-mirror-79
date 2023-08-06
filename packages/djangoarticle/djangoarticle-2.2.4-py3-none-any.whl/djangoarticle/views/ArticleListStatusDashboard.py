from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from djangoarticle.models import ArticleModelScheme


class ArticleListStatusDashboard(LoginRequiredMixin, ListView):
    template_name = "djangoadmin/djangoarticle/article_list_dashboard.html"
    context_object_name = "article_filter"
    paginate_by = 10

    def get_queryset(self, **kwargs):
        return ArticleModelScheme.objects.status(self.kwargs['status'], self.request.user)