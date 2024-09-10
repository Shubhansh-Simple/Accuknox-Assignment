# account_app/models.py

# local
from Core.utilities.models import CustomAbstractUser


########################
# USER'S ACCOUNT MODEL #
########################
class Account(CustomAbstractUser):
    '''Override django's default user model for adding more fields'''

    class Meta:
        db_table            = 'account_app_account'
        verbose_name        = 'Account'
        verbose_name_plural = 'Accounts'


    # For later use
    def clean(self): pass


    def save(self, *args, **kwargs):
        '''Handle field values before saving into the database'''
        
        # Calling clean method
        self.clean()

        super().save(*args, **kwargs)


    def __str__(self): return f'{self.email}'
