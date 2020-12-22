"""
User Model.
"""

from django.db import models


class User(models.Model):
    """
    Model for users.
    """
    display_name = models.CharField(max_length=35, blank=False, unique=True)
    user_id = models.UUIDField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=3, blank=False)

    def save(self, *args, **kwargs):
        """
        Save method overridden for making all country codes lower case.
        """
        self.country = self.country.lower()
        return super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = 'users'
