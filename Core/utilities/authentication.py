# Core/utilities/authentication.py

# django
from django.contrib.auth          import get_user_model
from django.contrib.auth.backends import ModelBackend


#######################################################
# OVERRIDE DEFAULT AUTHENTICATION PROCESS OF "DJANGO" #
#######################################################
class CustomModelBackend(ModelBackend):
    '''Authenticating the user using his email & password'''

    def authenticate(self, request, username=None, password=None, **kwargs):
        '''Check weather user exists with provided username ( i.e. email in this case) before matching the password'''

        # Mandatory fields for authenticate any user
        if username and password:

            UserModel = get_user_model()
            user      = None

            # No spaces allowed in email
            if ' ' not in username:

                # Getting user through their email ( insensitive )
                if '@' in username and '.' in username: user = UserModel.objects.filter(email__iexact=username)

                # Checking for user's password if user exists
                if user and user.exists() and user.first().check_password(password): return user.first()

        # No user exists with provided username (i.e. email) & password
        return None
