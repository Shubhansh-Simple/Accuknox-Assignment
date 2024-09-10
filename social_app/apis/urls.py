# social_app/apis/urls.py

# django
from django.urls import path

# local
from .views import FriendRequestSentAPIView, FriendListAPIView

urlpatterns = [
    path('', FriendListAPIView.as_view() ),
    path('request-sent/<int:pk>/',   FriendRequestSentAPIView.as_view() ),
    #path('request-accept/', FriendRequestAcceptAPIView.as_view() ),
    #path('request-reject/', FriendRequestRejectAPIView.as_view() ),
    #path('request-pending-list/',  FriendRequestPendingListAPIView.as_view() ),
]
