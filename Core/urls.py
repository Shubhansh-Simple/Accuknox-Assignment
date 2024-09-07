# Core/urls.py

# django
from django.contrib import admin
from django.urls    import path

urlpatterns = [

    # for admin site
    path('administration/', admin.site.urls),
]
