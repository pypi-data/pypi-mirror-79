from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from djangoarticle.managers import CategoryModelSchemeManager


class CategoryModelScheme(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
        ('withdraw', 'Withdraw'),
        ('private', 'Private')
    )
    serial        = models.IntegerField(blank=True, null=True)
    title         = models.CharField(max_length=35, unique=True, blank=False, null=False)
    slug          = models.SlugField(max_length=35, unique=True, blank=False, null=False)
    cover_image   = models.ImageField(null=True, blank=True, upload_to='uploads')
    description   = models.TextField(blank=True, null=True)
    author        = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    verification  = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    # call all the model managers.
    objects = CategoryModelSchemeManager()

    def __str__(self):
        return self.title

    # overright the save method.
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.serial is None:
            self.serial = self.pk 
        super(CategoryModelScheme, self).save(*args, **kwargs)

    # get the absolute urls.
    def get_absolute_url_for_detail_view(self):
        return reverse("djangoarticle:category_detail_view", kwargs={'category_slug': self.slug})

    def get_absolute_url_for_update_view(self):
        return reverse("djangoarticle:category_update_view", kwargs={'category_slug': self.slug})

    def get_absolute_url_for_delete_view(self):
        return reverse("djangoarticle:category_delete_view", kwargs={'category_slug': self.slug})

    class Meta:
        ordering            = ['-serial', '-pk']
        verbose_name        = 'Djangoarticle category'
        verbose_name_plural = 'Djangoarticle categories'