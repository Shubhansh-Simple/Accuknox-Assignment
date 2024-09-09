# social_app/apps.py

# django
from django.apps import AppConfig


class SocialAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name               = 'social_app'
    verbose_name       = 'Social Networking Section'
