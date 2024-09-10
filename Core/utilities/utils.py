# Core/utilities/utils.py

# python
import datetime

# django
from django.contrib.auth import get_user_model


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


##############################
# CHECK USER EXISTS & ACTIVE #
##############################
def IsUserExistsAndActive(user_id):
    '''Check weather user exists and is active for a given user_id'''

    # Return None if input is invalid
    if not isinstance(user_id, int): return None

    # Check if a user exists with the given ID and is active
    return get_user_model().objects.filter(id=user_id, is_active=True).exists()
