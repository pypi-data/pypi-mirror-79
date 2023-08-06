from django.apps import AppConfig


class DjangoarticleConfig(AppConfig):
    name = 'djangoarticle'

    def ready(self):
        import djangoarticle.signals
