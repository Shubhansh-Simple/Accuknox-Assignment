# social_app/utils.py

# local
from Core.utilities.utils import STATUS_CHOICES
from social_app.models    import FriendRequest


##############################
# GET PENDING FRIEND REQUEST #
##############################
def GetPendingFriendRequest(pk, user_id):
    '''Return pending friend request using id (i.e. pk) recieved by user (specified by user_id)'''

    # Return None if input is invalid
    if not isinstance(pk, int) or not isinstance(user_id, int): return None

    # Return recieved friend request record if exists and in 'pending' status
    try:
        return FriendRequest.objects.get(id=pk, reciever_id=user_id, status=STATUS_CHOICES[0][0])
    except FriendRequest.DoesNotExist:
        return None
