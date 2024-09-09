# account_app/apis/views.py

'''
LIST OF VIEW CLASSES IN THIS FILE
    - AccountLoginAPIView
    - AccountSignupAPIView
'''

# django
from django.contrib.auth import authenticate

# rest_framework
from rest_framework          import status
from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

# simplejwt
from rest_framework_simplejwt.tokens import RefreshToken

# local
from .serializers import AccountLoginSerializer, AccountSignupSerializer


##################
# LOGIN ENDPOINT #
##################
class AccountLoginAPIView(APIView):
    '''
    User can able authenticate through this view and get a JWT token

    --------------------------------------------------
    METHOD  - POST
    URL     - /login
    PAYLOAD - {...}
    ALLOWED - AllowAny

    Payload Example
        {
            "username" : "someone@gmail.com",
            "password" : "something@123"
        }

    Response Example
        {
            "id"       : 1,
            "access"   : "Your access token",
            "refresh"  : "Your refresh token"
        }
    '''

    permission_classes = []         # any one able to access this view

    def post(self, request):
        '''Authenticate the user using this email & password then only return access token'''

        print('Request.data - ',request.data)

        serializer = AccountLoginSerializer(data=request.data)

        if serializer.is_valid():

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Authenticating the user
            authenticate_user = authenticate(username=username, password=password)

            # User Found
            if authenticate_user:

                refresh_token = RefreshToken.for_user(authenticate_user)
                access_token  = refresh_token.access_token

                # Preparing response
                response = {
                    "id"      : authenticate_user.id,
                    "access"  : str(access_token),
                    "refresh" : str(refresh_token)
                }

                # Success Message
                return Response(response, status=status.HTTP_200_OK)

            # User Not Found
            return Response({"detail" : "Invalid username or password. Please try again."}, status=status.HTTP_401_UNAUTHORIZED)

        # Bad request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###################
# SIGNUP ENDPOINT #
###################
class AccountSignupAPIView(CreateAPIView):
    '''
    Create the account for the users

    --------------------------------------------------
    METHOD  - POST
    URL     - /signup
    PAYLOAD - {...}
    ALLOWED - AllowAny
    '''

    permission_classes = []         # any one able to access this view

    def create(self, request, *args, **kwargs):
        '''
        Payload Example
            {
                "username"         : "something@gmail.com",
                "password"         : "Your-password-here",
                "confirm_password" : "Your-confirm-password-here"
            }

        Response Example
            {
                "id"     : 1,
                "detail" : "User created successfully"
            }
        '''

        print('Request.data - ',request.data)

        serializer = AccountSignupSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            # Response
            response = {
                "id"     : user.id,
                "detail" : f"{user.email}'s account created successfully"
            }

            # Success Message
            return Response(response, status=status.HTTP_201_CREATED)

        # Bad request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
