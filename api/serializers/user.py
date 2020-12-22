"""
UserSerializer class.
"""

from rest_framework import serializers

from api.models.user import User


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """
    class Meta:
        model = User
        fields = ['user_id', 'display_name', 'country']
