# Core/utilities/models.py

'''
LIST OF UTILITY CLASSES IN THIS FILE
    - CustomAbstractUser
'''

# django
from django.db                      import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models     import AbstractUser, BaseUserManager


############################
# CUSTOM BASE USER MANAGER #
############################
class CustomBaseUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        '''Creating the user using email & encrypted password'''

        # Email is mandatory for creating the user
        if not email: raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)

        # storing encrypted password
        user.set_password(password)

        user.save(using=self._db)

        return user


    def create_superuser(self, email, password=None, **extra_fields):
        '''Creating the superuser with staff & superuser status must be true'''

        # for superuser only
        extra_fields.setdefault('is_staff',     True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


##############################
# CUSTOM ABSTRACT USER MODEL #
##############################
class CustomAbstractUser(AbstractUser):
    '''
    Override default Django User model and use it as Parent Class of all database model class
    Note : It's an abstract class to save code repeatition and will not used for creating database table

    Attributes - 12
        
        # DEFAULT FIELDS
            - id
            - username
            - email
            - password
            - first_name
            - last_name
            - last_login
            - is_active
            - is_staff
            - is_superuser
        
        # ADDITIONAL FIELDS
            - created_at
            - updated_at
    '''

    # OVERRIDE
    username = models.CharField( max_length=150, 
                                 unique=True, 
                                 null=True,
                                 blank=True,
                                 validators=[UnicodeUsernameValidator],
                                 help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                 error_messages={'unique' : 'A user with that username already exists.'})

    # OVERRIDE
    email    = models.EmailField(max_length=254, unique=True)

    # Removing unnecessary field
    date_joined = None

    # EXTRA FIELDS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Email will be treated as username
    USERNAME_FIELD = 'email'

    # Below fields will pop ( on command prompt ) while creating superuser with default fields
    REQUIRED_FIELDS = []

    objects = CustomBaseUserManager()

    class Meta:
        abstract = True    # Ensure this model is not used for creating a database table
