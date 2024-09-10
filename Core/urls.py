# Core/urls.py

# django
from django.contrib import admin
from django.urls    import path, include


urlpatterns = [

    # for admin site
    path('administration/', admin.site.urls),

    # for account app
    path('friends/', include('social_app.apis.urls') ),

    # for social app
    path('users/', include('account_app.apis.urls') ),
]

# Updating Admin Site's Page Title
admin.site.site_header = 'Accuknox Backend Assignment'
admin.site.index_title = 'Administration Site'
