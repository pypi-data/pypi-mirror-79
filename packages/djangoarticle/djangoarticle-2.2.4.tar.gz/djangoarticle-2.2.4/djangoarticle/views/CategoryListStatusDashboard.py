from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from djangoarticle.models import CategoryModelScheme


class CategoryListStatusDashboard(LoginRequiredMixin, ListView):
    template_name = "djangoadmin/djangoarticle/category_list_dashboard.html"
    context_object_name = "category_list"
    paginate_by = 10

    def get_queryset(self, **kwargs):
        return CategoryModelScheme.objects.status(self.kwargs['status'], self.request.user)