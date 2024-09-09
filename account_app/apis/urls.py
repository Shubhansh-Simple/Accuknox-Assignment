# account_app/apis/urls.py

# django
from django.urls import path

# local
from .views import AccountLoginAPIView, AccountSignupAPIView

urlpatterns = [
    path('login/',  AccountLoginAPIView.as_view() ),
    path('signup/', AccountSignupAPIView.as_view() ),
]
