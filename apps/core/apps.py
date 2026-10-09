"""
Core app configuration — Code Yari
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Core'

    def ready(self):
        from django.db.models.signals import post_migrate
        from .auto_seed import auto_seed_on_migrate
        post_migrate.connect(auto_seed_on_migrate, sender=self)
