# account_app/apps.py

# django
from django.apps import AppConfig


class AccountAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name               = 'account_app'
    verbose_name       = 'User Account Section'
