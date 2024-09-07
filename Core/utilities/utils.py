# Core/utilities/utils.py

# python
import datetime


##################################
# CURRENT DATETIME WITH TIMEZONE #
##################################
def get_current_time_with_tz():
    '''Return current datetime with timezone'''

    timezone = datetime.timezone.utc
    return datetime.datetime.now(timezone)
