"""
Django Admin.
"""

from django.contrib import admin
from .models.user import User
from .models.user_score import UserScore


class UserAdmin(admin.ModelAdmin):
    """
    Customize user admin.
    """
    search_fields = ['user_id']


class UserScoreAdmin(admin.ModelAdmin):
    """
    Customize user-score admin.
    """
    search_fields = ['user_id__user_id']


admin.site.register(User, UserAdmin)
admin.site.register(UserScore, UserScoreAdmin)
