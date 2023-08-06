from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from djangoarticle.models import ArticleModelScheme
from djangoarticle.modelforms import ArticleModelFormScheme
from djangoarticle.mixins import AdministratorAndOnlyAuthorAccess


class ArticleUpdateView(LoginRequiredMixin, AdministratorAndOnlyAuthorAccess, SuccessMessageMixin, UpdateView):
    model = ArticleModelScheme
    form_class = ArticleModelFormScheme
    template_name = 'djangoadmin/djangoarticle/article_create_view_form.html'
    success_url = reverse_lazy('djangoarticle:article_list_dashboard')
    slug_url_kwarg = 'article_slug'
    success_message = "article updated successfully."

    def get_success_message(self, cleaned_data):
        return f"{cleaned_data['title']} {self.success_message}"

    def form_valid(self, form):
        form.instance.author = form.instance.author
        form.save()
        return super(ArticleUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        context['article_form'] = context['form']
        return context