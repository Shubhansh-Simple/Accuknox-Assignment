# Core/utilities/serializers.py

'''
LIST OF UTILITIES SERIALIZER CLASSES IN THIS FILE
    - BaseSignupSerializer
'''

# django
from django.contrib.auth                     import get_user_model
from django.contrib.auth.password_validation import validate_password

# rest_framework
from rest_framework            import serializers
from rest_framework.validators import ValidationError, UniqueValidator


##########################
# BASE SIGNUP SERIALIZER #
##########################
class BaseSignupSerializer(serializers.ModelSerializer):
    '''
    Serialize common fields for signup from AUTH_USER_MODEL i.e. Account Model ( which can be overriden later ! )

    Payload
        {
            "username"         : "something@email.com",
            "password"         : "Your-password-here",
            "confirm_password" : "Your-confirm-password-here"
        }
    '''

    # WRITE-ONLY PARENT SERIALIZER

    # OVERRIDE
    username         = serializers.EmailField(max_length=254,
                                             required=True,
                                             write_only=True,
                                             validators=[UniqueValidator(queryset=get_user_model().objects.all())])

    # EXTRA FIELD
    confirm_password = serializers.CharField(max_length=128, required=True, write_only=True)


    class Meta:
        model        = get_user_model()
        fields       = ['username', 'password', 'confirm_password']
        extra_kwargs = {
            'password' : {'write_only' : True, 'required' : True}
        }


    def validate_username(self, value):
        '''Remove unwanted spaces from username'''

        self.email = value.strip()                      # store it for later user
        return self.email


    def validate_password(self, value):
        '''Check password strongness against django built-in password validators'''

        # Create an sample user instance to make the UserAttributeSimilarityValidator works
        sample_user = get_user_model()(email=getattr(self, 'email', None))

        validate_password(value, user=sample_user)      # will raise ValidationError with all errors at once

        return value


    def validate(self, attrs):
        '''Ensuring the equality of password & confirm_password'''

        errors = {}

        # removing unnecessary field
        confirm_password = attrs.pop('confirm_password')

        # Check for password match
        if attrs['password'] != confirm_password: errors['confirm_password'] = "Password doesn't match"

        # Raise multi errors at once
        if errors: raise ValidationError(errors)

        return attrs
