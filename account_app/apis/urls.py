# account_app/apis/urls.py

# django
from django.urls import path

# local
from .views import AccountLoginAPIView,\
                   AccountSignupAPIView,\
                   UserListAPIView

urlpatterns = [
    path('',        UserListAPIView.as_view() ),
    path('login/',  AccountLoginAPIView.as_view() ),
    path('signup/', AccountSignupAPIView.as_view() )
]
