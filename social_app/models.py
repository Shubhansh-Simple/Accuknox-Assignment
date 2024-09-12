# social_app/models.py

# django
from django.db           import models
from django.contrib.auth import get_user_model

# local
from Core.utilities.utils import STATUS_CHOICES


########################
# FRIEND REQUEST MODEL #
########################
class FriendRequest(models.Model):
    '''Storing friend requests of users'''

    sender     = models.ForeignKey(get_user_model(), related_name='sent_requests',     on_delete=models.CASCADE)
    reciever   = models.ForeignKey(get_user_model(), related_name='recieved_requests', on_delete=models.CASCADE)
    status     = models.CharField(max_length=8, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    created_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together     = ('sender', 'reciever')
        verbose_name        = 'Friend Request'
        verbose_name_plural = 'Friend Requests'


    def __str__(self): return f'{self.sender} - {self.reciever} {[self.status]}'


####################
# FRIENDSHIP MODEL #
####################
class Friendship(models.Model):
    '''Storing friendship between two users'''

    user1      = models.ForeignKey(get_user_model(), related_name='friends_user1', on_delete=models.CASCADE)
    user2      = models.ForeignKey(get_user_model(), related_name='friends_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together     = ('user1', 'user2')
        verbose_name        = 'Friendship'
        verbose_name_plural = 'Friendships'


    def __str__(self): return f'{self.user1} - {self.user2}'
