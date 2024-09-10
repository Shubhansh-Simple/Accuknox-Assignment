# social_app/apis/views.py

'''
LIST OF VIEW CLASSES IN THIS FILE
    - FriendRequestSentAPIView
    - FriendRequestAcceptAPIView
    - FriendRequestRejectAPIView
    - FriendListAPIView
    - FriendRequestPendingListAPIView
'''

# django
from django.db.models import Q

# rest_framework
from rest_framework          import status
from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

# local
from Core.utilities.utils import IsUserExistsAndActive, STATUS_CHOICES
from social_app.models    import FriendRequest, Friendship
from .serializers         import FriendListSerializer


class FriendRequestSentAPIView(APIView):
    '''
    User able to send friend request to any active users ( specified by pk ) through this view

    --------------------------------------------------
    METHOD  - POST
    URL     - /request-sent/<int:pk>
    PAYLOAD - {}
    ALLOWED - Authenticate User

    Workflow:
        - Checks if the recipient user (identified by `pk`) exists and is active.
        - If a friend request already exists between the users, it verifies the status:
            . If 'pending', it returns a message indicating the request is already pending.
            . If 'accepted', it returns a message indicating the request has already been accepted.
            . If 'rejected', it updates the status back to 'pending' and re-sends the friend request.
        - If no friend request exists, a new one is created.

    Possible Response Example:

        # If request is pending
        {"detail" : "Friend request is already pending", status=400}

        # If request was accepted
        {"detail" : "You are already friends", status=400}

        # If request was rejected
        {"detail" : "Friend request has been re-sent", status=200}

        # No friend request exists
        {"detail" : Friend request sended successfully", status=200}
    '''

    def post(self, request, pk):

        # Debugging
        print('Value of pk - ',pk)
        print('Requested user - ',request.user, request.user.id)

        # Prevent user from sending a friend request to themselves
        if request.user.id == pk:
            return Response({"detail": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # User must exists & be active
        if not IsUserExistsAndActive(pk):
            return Response({"detail" : "User not found or in-active"}, status=status.HTTP_404_NOT_FOUND)

        # Check if friend request record exists already
        try:
            friend_request = FriendRequest.objects.get(
                                Q(sender_id=request.user.id, reciever_id=pk) | Q(sender_id=pk, reciever_id=request.user.id)
                             )
        except FriendRequest.DoesNotExist:
            friend_request = None

        print('Queryset - ',friend_request)

        # If friend request exists already
        if friend_request:

            # Request is pending
            if friend_request.status == STATUS_CHOICES[0][0]:     # 'pending'
                return Response({"detail" : "Friend request is already pending"}, status=status.HTTP_400_BAD_REQUEST)

            # Request was accepted
            elif friend_request.status == STATUS_CHOICES[1][0]:   # 'accepted'
                return Response({"detail" : "You are already friends"}, status=status.HTTP_400_BAD_REQUEST)

            # Request was rejected, resending it
            elif friend_request.status == STATUS_CHOICES[2][0]:   # 'rejected'

                # Change status from 'rejected' to 'pending'
                friend_request.status = STATUS_CHOICES[0][0]      # 'pending'
                friend_request.save()

                return Response({"detail" : "Friend request has been re-sent"}, status=status.HTTP_200_OK)

        # No friend request exists, create a new one
        try:
            FriendRequest.objects.create( sender_id=request.user.id, reciever_id=pk )
            return Response({"detail" : "Friend request sended successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            print('Exception raised - ',e)                      # Debugging

            # Error
            error       = {"detail" : "Unable to send friend request. Please try again later"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            # Internal Server Error
            return Response(error, status=status_code)




















######################
# FRIENDLIST APIVIEW #
######################
class FriendListAPIView(ListAPIView):

    pass
