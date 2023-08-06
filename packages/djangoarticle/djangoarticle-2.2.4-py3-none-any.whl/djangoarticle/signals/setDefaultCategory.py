from django.db.models.signals import pre_delete
from django.contrib.auth.models import User
from djangoarticle.models import CategoryModelScheme
from djangoarticle.models import ArticleModelScheme


def setDefaultCategory(sender, instance, using, **kwargs):
    try:
        adtr = User.objects.get(pk=1)
    except:
        adtr = None
    obj, created = CategoryModelScheme.objects.get_or_create(title="Default", author=adtr, verification=True, status="publish")
pre_delete.connect(setDefaultCategory, sender=CategoryModelScheme)