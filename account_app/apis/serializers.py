# account_app/apis/serializers.py

'''
LIST OF SERIALIZER CLASSES IN THIS FILE

    - AccountLoginSerializer
    - AccountSignupSerialzer
'''

# django
from django.db           import IntegrityError
from django.contrib.auth import get_user_model

# rest_framework
from rest_framework            import serializers
from rest_framework.validators import ValidationError

# local
from Core.utilities.serializers import BaseSignupSerializer


############################
# ACCOUNT LOGIN SERIALIZER #
############################
class AccountLoginSerializer(serializers.Serializer):
    '''Serialize username ( i.e. email ) & password'''

    # WRITE-ONLY SERIALIZER

    username = serializers.EmailField( max_length=254, required=True, write_only=True )
    password = serializers.CharField(  max_length=128, required=True, write_only=True )

    # Removing unnecessary spaces
    def validate_username(self, value): return value.strip()


#############################
# ACCOUNT SIGNUP SERIALIZER #
#############################
class AccountSignupSerializer(BaseSignupSerializer):
    '''
    Serialize fields for signup from AUTH_USER_MODEL i.e. Account Model

    Payload
        {
            "username"         : "something@email.com",          # i.e. email in this case
            "password"         : "Your-password-here",
            "confirm_password" : "Your-confirm-password-here"
            "first_name"       : "shubham",
            "last_name"        : "tripathi"
        }

    '''
    # WRITE ONLY SERIALIZER

    def validate(self, attrs):

        attrs = super().validate(attrs)

        # Renaming the username field for database saving
        attrs['email'] = attrs.pop('username')

        return attrs


    def create(self, validated_data):
        '''Create the user's account by using manager's create_user() method''' 

        User = get_user_model()

        try:
            return User.objects.create_user(**validated_data)
        except IntegrityError:
            raise ValidationError({"detail" : "User with this email already exists."})    # Handle duplicate email address


########################
# USER LIST SERIALIZER #
########################
class UserListSerializer(serializers.ModelSerializer):
    '''Serializer common fields for listing users'''

    class Meta:
        model  = get_user_model()

        # Showing only limited fields for simplicity
        fields           = ['id', 'email', 'first_name', 'last_name', 'is_active', 'created_at']
        read_only_fields = fields.copy()
