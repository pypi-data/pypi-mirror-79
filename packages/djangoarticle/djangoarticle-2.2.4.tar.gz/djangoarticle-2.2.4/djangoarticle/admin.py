from django.contrib import admin
from djangoarticle.models import CategoryModelScheme
from djangoarticle.models import ArticleModelScheme
from djangoarticle.models import ArticleBookmarkModelScheme
from djangoarticle.modeladmins import CategoryModelSchemeAdmin
from djangoarticle.modeladmins import ArticleModelSchemeAdmin
from djangoarticle.modeladmins import ArticleBookmarkModelSchemeAdmin


# Register your models here.
admin.site.register(CategoryModelScheme, CategoryModelSchemeAdmin)
admin.site.register(ArticleModelScheme, ArticleModelSchemeAdmin)
admin.site.register(ArticleBookmarkModelScheme, ArticleBookmarkModelSchemeAdmin)