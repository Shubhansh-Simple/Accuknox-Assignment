# social_app/apis/views.py

'''
LIST OF VIEW CLASSES IN THIS FILE
    - FriendListAPIView
    - FriendRequestSentAPIView
    - FriendRequestAcceptAPIView
    - FriendRequestRejectAPIView
    - FriendRequestPendingListAPIView
'''

# django
from django.db           import transaction
from django.db.models    import Q
from django.contrib.auth import get_user_model

# rest_framework
from rest_framework          import status
from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

# local
from Core.utilities.utils         import IsUserExistsAndActive, STATUS_CHOICES
from account_app.apis.serializers import UserListSerializer
from social_app.models            import FriendRequest, Friendship
from social_app.utils             import GetPendingFriendRequest
from .serializers                 import FriendRequestPendingListSerializer


####################
# FRIEND LIST VIEW #
####################
class FriendListAPIView(ListAPIView):
    '''
    List of users who are friend of requested user

    --------------------------------------------------
    METHOD  - GET
    URL     - /
    PAYLOAD - {}
    ALLOWED - Authenticate User

    Response Example
        [
            {
                "id"         : 1,
                "email"      : "someone@gmail.com",
                "first_name" : "Someone",
                "last_name"  : "Random",
                "is_active"  : true,
                "created_at" : "2024-09-07T21:42:08.154814+05:30"
            },
            {...}, {...}, {...}
        ]
    '''

    serializer_class = UserListSerializer

    def get_queryset(self):
        '''Return friend list of the authenticated user'''

        requested_user_id = self.request.user.id

        # Fetching IDs where the user is either user1 or user2
        friendship_ids = Friendship.objects.filter(
                            Q(user1_id=requested_user_id) | Q(user2_id=requested_user_id)
                         ).values_list('user1', 'user2')

        # Collecting all unique friends ids
        friend_ids = set()

        for user1_id, user2_id in friendship_ids:

            # If the current user is user1, the friend is user2, and vice versa
            friend_ids.add( user2_id if user1_id == requested_user_id else user1_id)

        # Fetching all User objects for these IDs
        return get_user_model().objects.filter(
                    id__in=friend_ids
               ).values('id', 'email', 'first_name', 'last_name', 'is_active', 'created_at')


###############################
# FRIEND REQUEST SENT APIVIEW #
###############################
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


#################################
# FRIEND REQUEST ACCEPT APIVIEW #
#################################
class FriendRequestAcceptAPIView(APIView):
    '''
    Users able to accept their recieved pending friend request from other users through this view

    --------------------------------------------------
    METHOD  - POST
    URL     - /request-accept/<int:pk>
    PAYLOAD - {}
    ALLOWED - Authenticate User

    Response Example
        {
            "detail" : "Friend request accepted successfully"
        }
    '''

    def post(self, request, pk):

        # Get recieved pending friend request
        friend_request = GetPendingFriendRequest(pk, request.user.id)
        print('Friend request - ',friend_request)

        # No pending friend request exists
        if not friend_request:
            return Response({"detail" : "No pending friend request found"}, status=status.HTTP_404_NOT_FOUND)

        # Friend request exists
        try:
            with transaction.atomic():

                # Change friend request status to 'accepted' ( in FriendRequest Model )
                friend_request.status = STATUS_CHOICES[1][0]   # 'accepted'
                friend_request.save()

                # Make them friend ( in Friendship Model )
                Friendship.objects.create(user1_id=request.user.id, user2_id=friend_request.sender_id)

                # Success Message
                return Response({"detail" : "Friend request accepted successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            print('Exception raised - ',e)                     # Debugging

            # Error
            error       = {"detail" : "Unable to accept friend request. Please try again later"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            # Internal Server Error
            return Response(error, status=status_code)


#################################
# FRIEND REQUEST REJECT APIVIEW #
#################################
class FriendRequestRejectAPIView(APIView):
    '''
    User able to reject recieved pending friend request of other users
    --------------------------------------------------
    METHOD  - POST
    URL     - /request-reject/<int:pk>
    PAYLOAD - {}
    ALLOWED - Authenticate User

    Response Example
        {
            "detail" : "Friend request rejected successfully"
        }
    '''

    def post(self, request, pk):

        # Get recieved pending friend request
        friend_request = GetPendingFriendRequest(pk, request.user.id)

        # No pending friend request exists
        if not friend_request:
            return Response({"detail" : "No pending friend request found"}, status=status.HTTP_404_NOT_FOUND)

        # Friend request exists
        try:
            friend_request.status = STATUS_CHOICES[2][0]   # 'rejected'
            friend_request.save()

            # Success Message
            return Response({"detail" : "Friend request rejected successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            print('Exception raised - ',e)                 # Debugging

            # Error
            error       = {"detail" : "Unable to reject friend request. Please try again later"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            # Internal Server Error
            return Response(error, status=status_code)


#######################################
# FRIEND REQUEST PENDING LIST APIVIEW #
#######################################
class FriendRequestPendingListAPIView(ListAPIView):
    '''
    User can see all pending friend requests received by them

    --------------------------------------------------
    METHOD  - GET
    URL     - /request-pending-list
    PAYLOAD - {}
    ALLOWED - Authenticate User

    Response Example
        [
            {
                "id"         : 13,
                "sender"     : "someone@gmail.com",
                "created_at" : "2024-09-12T19:59:33.293090+05:30"
            },
            {...}, {...}, {...}
        ]
    '''

    serializer_class = FriendRequestPendingListSerializer

    def get_queryset(self):
        '''Return pending friend requests received by the authenticated user'''

        return FriendRequest.objects.filter(
                reciever_id=self.request.user.id,
                status=STATUS_CHOICES[0][0]               # 'pending'
        ).values('id', 'sender__email', 'created_at')
