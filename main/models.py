from django.contrib.auth.models import User
from django.db import models


class UserData(models.Model):
    """
    Master user table
    All the user data will be saved here.
    """
    # Link django user instance (Note: Password will be saved inside default django user instance)
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='Unique user django instance')
    # Optional Email Field
    email = models.EmailField(null=True, blank=True, help_text='Optional user\'s email')
    # Optional Mobile Field
    mobile = models.BigIntegerField(null=True, blank=True, help_text='Optional user\'s mobile')

    # Time stamp fields for future some usecase purpose
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return "%s" % self.user.username
