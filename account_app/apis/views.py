# account_app/apis/views.py

'''
LIST OF VIEW CLASSES IN THIS FILE
    - AccountLoginAPIView
    - AccountSignupAPIView
    - UserSearchByEmailAndName
'''

# django
from django.db.models       import Q
from django.contrib.auth    import authenticate, get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# rest_framework
from rest_framework          import status
from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView

# simplejwt
from rest_framework_simplejwt.tokens import RefreshToken

# local
from Core.utilities.utils   import IsOnlyChar
from .serializers           import AccountLoginSerializer, AccountSignupSerializer, UserListSerializer


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


###############################
# USER SEARCH BY EMAIL & NAME #
###############################
class UserListAPIView(ListAPIView):
    '''
    Retrieves the list of users, excluding the current user.

    If a search keyword is provided:
      - Filters users by an exact match on email (case-insensitive),
      - Or partial matches on first name or last name (case-insensitive).

    If no search keyword is provided, the method returns the entire list of users (excluding the current user)

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
        search_keyword = self.request.query_params.get('q', '').strip()
        User           = get_user_model()

        print(f'Search keyword - "{search_keyword}", {len(search_keyword)}, {type(search_keyword)}')

        # Apply search conditions
        if search_keyword:

            # SEARCH BY NAMES #
            if IsOnlyChar(search_keyword):
                '''Assuming names can only contain letters (i.e. a-z or A-Z) and spaces'''

                # Search user by first_name or last_name
                return User.objects.filter(
                            Q(first_name__icontains=search_keyword) |  # Partial match for first_name
                            Q(last_name__icontains=search_keyword)     # Partial match for last_name
                       )

            # SEARCH BY EMAIL #
            try:
                validate_email(search_keyword)                               # Avoid querying database for invalid emails
                return User.objects.filter(email__iexact=search_keyword)     # Exact email match, case-insensitive
            except ValidationError:
                pass

            # Return empty queryset, if not match found
            return User.objects.none()

        # If no search_keyword provided return all users excluding requested user
        else: return User.objects.exclude(id=self.request.user.id)


    def list(self, request, *args, **kwargs):
        '''Adding pagination later'''

        #queryset = self.get_queryset()
        return super().list(request, *args, **kwargs)
