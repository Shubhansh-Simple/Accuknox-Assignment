# social_app/admin.py

# django
from django.contrib import admin
from django.forms   import ValidationError

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

    def save_model(self, request, obj, form, change):

        # Check weather sender and reciever are the same person
        if obj.sender == obj.reciever: raise ValidationError('You cannot friend request to yourself.')

        # Save the model if no error raised
        return super().save_model(request, obj, form, change)

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

    def save_model(self, request, obj, form, change):

        # Check weather sender and reciever are the same person
        if obj.user1 == obj.user2: raise ValidationError('You cannot become friend of yourself.')

        # Save the model if no error raised
        return super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Friendship, FriendshipAdmin)
