# social_app/apis/urls.py

# django
from django.urls import path

# local
from .views import \
        FriendRequestSentAPIView,\
        FriendRequestAcceptAPIView,\
        FriendListAPIView

urlpatterns = [
    path('', FriendListAPIView.as_view() ),
    path('request-sent/<int:pk>/',          FriendRequestSentAPIView.as_view() ),
    path('request-accept/<int:pk>/',        FriendRequestAcceptAPIView.as_view() ),
    #path('request-reject/', FriendRequestRejectAPIView.as_view() ),
    #path('request-pending-list/',  FriendRequestPendingListAPIView.as_view() ),
]
