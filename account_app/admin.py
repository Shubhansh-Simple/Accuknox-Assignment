# account_app/admin.py

# django
from django.contrib                 import admin
from django.contrib.sessions.models import Session

# local
from Core.utilities.utils import get_current_time_with_tz
from .models              import Account


########################
# USER'S ACCOUNT MODEL #
########################
class AccountAdmin(admin.ModelAdmin):
    '''Modify Account model representation on admin site'''

    # To improve visibility in admin site
    readonly_fields = ('id', 'password',)
    list_display    = ('email', 'is_active', 'first_name', 'last_name', 'id')

# Register your models here.
admin.site.register(Account, AccountAdmin)


#################################
# Django in-built Session Model #
#################################
class SessionAdmin(admin.ModelAdmin):
    '''Modify In-built Django's Session model representation on admin site'''

    # To improve visibility in admin site
    readonly_fields = ('_session_data', 'session_key')
    list_display    = ('session_key', '_session_data', 'expire_date', 'expired',)

    def _session_data(self, obj): return obj.get_decoded()

    @admin.display(
        boolean    = True,
        description= 'Validity'
    )
    def expired(self, obj): return obj.expire_date > get_current_time_with_tz()

# Register your models here.
admin.site.register(Session, SessionAdmin)
