# Core/utilities/utils.py

'''
LIST OF CONSTANT, FUNCTION & CLASSES IN THIS FILE
    - STATUS_CHOICES
    - get_current_time_with_tz
    - CustomPageNumberPagination
    - IsUserExistsAndActive
    - IsOnlyChar
'''

# python
import datetime

# django
from django.contrib.auth import get_user_model

# rest_framework
from rest_framework.response   import Response
from rest_framework.pagination import PageNumberPagination


#################################
# FRIEND REQUEST STATUS CHOICES #
#################################
STATUS_CHOICES = [
    # NOTE : SEQUENCE OF LIST ITEMS MATTERS HERE!

    ('pending', 'Pending'),   # [0]
    ('accepted', 'Accepted'), # [1]
    ('rejected', 'Rejected')  # [2]
]


##################################
# CURRENT DATETIME WITH TIMEZONE #
##################################
def get_current_time_with_tz():
    '''Return current datetime with timezone'''

    timezone = datetime.timezone.utc
    return datetime.datetime.now(timezone)


#################################
# CUSTOM PAGE NUMBER PAGINATION #
#################################
class CustomPageNumberPagination(PageNumberPagination):
    '''
    Custom page number pagination to paginate the queryset into small datasets
    
    For eg  - To fetch the record of second page with 5 records per page, we will use following url
        URL - "http://192.168.43.98:8000/users/?page=2&page_size=5"

    Response Example
        {
            "count"    : 3,
            "next"     : "http://192.168.43.98:8000/users/?page=2&page_size=2&q=ch",
            "previous" : null,
            "detail"   : [
                {
                    "id": 3,
                    "email": "himanshu@gmail.com",
                    "first_name": "himanshu",
                    "last_name": "chourasia",
                    "is_active": true,
                    "created_at": "2024-09-12T19:26:09.142974+05:30"
                },
                {...}, {...}, {...}
            ]
        }
    '''

    page_size             = 10
    page_size_query_param = 'page_size'   # ?page_size=10, to mention total records per page
    max_page_size         = 10

    def get_paginated_response(self, data):
        '''Return following response format for paginated result'''

        return Response({
            'count'    : self.page.paginator.count,      # total records found
            'next'     : self.get_next_link(),           # next paginated page link
            'previous' : self.get_previous_link(),       # previous paginated page link
            'detail'   : data                            # actual data from database
        })


##############################
# CHECK USER EXISTS & ACTIVE #
##############################
def IsUserExistsAndActive(user_id):
    '''Check weather user exists and is active for a given user_id'''

    # Return None if input is invalid
    if not isinstance(user_id, int): return None

    # Check if a user exists with the given ID and is active
    return get_user_model().objects.filter(id=user_id, is_active=True).exists()


################
# IS ONLY CHAR #
################
def IsOnlyChar(keyword):
    '''
    Ensure the names only contains letters (i.e. a-z & A-Z) and spaces but no digit or special characters
    Return False on founding any digits or special characters else return True

    for eg. 'Shubham Tripathi' is an valid name
            'Shubham77' or '$hubh@m_Tripathi' are invalid names
    '''

    if keyword:

        # Check for each character in provided keyword
        for character in keyword:

            if not character.isspace() and not character.isalpha(): return False

        return True
