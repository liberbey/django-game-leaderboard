"""
UserScore Serializer class.
"""
from datetime import datetime

from rest_framework import serializers

from api.models.user import User
from api.models.user_score import UserScore


class UserScoreSerializer(serializers.ModelSerializer):
    """
    UserScore serializer.
    """

    class Meta:
        model = UserScore
        fields = ['user_id', 'score_worth', 'timestamp']
