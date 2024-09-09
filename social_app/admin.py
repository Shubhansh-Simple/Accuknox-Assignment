# social_app/admin.py

# django
from django.contrib import admin

# local
from .models import FriendRequest, Friendship


########################
# FRIEND REQUEST MODEL #
########################
class FriendRequestAdmin(admin.ModelAdmin):
    '''Modify Account model representation on admin site'''

    # To improve visibility in admin site
    readonly_fields = ('id', )
    list_display    = ('sender', 'reciever', 'status', 'created_at', 'id')

# Register your models here.
admin.site.register(FriendRequest, FriendRequestAdmin)


####################
# FRIENDSHIP MODEL #
####################
class FriendshipAdmin(admin.ModelAdmin):
    '''Modify Account model representation on admin site'''

    # To improve visibility in admin site
    readonly_fields = ('id', )
    list_display    = ('user1', 'user2', 'created_at', 'id')

# Register your models here.
admin.site.register(Friendship, FriendshipAdmin)
