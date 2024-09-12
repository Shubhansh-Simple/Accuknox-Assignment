# social_app/apis/serializers.py

'''
LIST OF SERIALIZER CLASSES IN THIS FILE

    - FriendListSerializer
'''

# django
from django.contrib.auth import get_user_model

# rest_framework
from rest_framework import serializers

# local
from social_app.models import FriendRequest


##########################
# FRIEND LIST SERIALIZER #
##########################
class FriendListSerializer(serializers.ModelSerializer):
    '''Serializer for listing friends of requested user'''

    class Meta:
        model   = get_user_model()

        # Showing only limited fields for simplicity
        fields  = ['id', 'email', 'first_name', 'last_name', 'is_active', 'created_at']


##########################################
# FRIEND REQUEST PENDING LIST SERIALIZER #
##########################################
class FriendRequestPendingListSerializer(serializers.ModelSerializer):
    '''Serializer for listing pending friend requests with string representation of the sender'''

    # Friend request sender
    sender   = serializers.CharField(source='sender__email', read_only=True)

    class Meta:
        model            = FriendRequest
        fields           = ['id', 'sender', 'created_at']
        read_only_fields = fields.copy()
