from django import template
from djangoarticle.models import ArticleModelScheme


register = template.Library()


@register.filter(name="check_bookmark")
def check_bookmark(slug, username):
    article = ArticleModelScheme.objects.get(slug=slug)
    if article.bookmarks.filter(username=username):
        return 'material-icons'
    else:
        return 'material-icons-outlined'