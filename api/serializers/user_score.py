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

    def to_internal_value(self, data):
        if 'timestamp' in data:
            try:
                datetime_val = datetime.fromtimestamp(int(data['timestamp']))
            except ValueError:
                raise serializers.ValidationError(
                    'timestamp must be valid.'
                )
            user = User.objects.filter(user_id=data['user_id'])
            return {"user_id": user[0],
                    "score_worth": data["score_worth"],
                    "timestamp": datetime_val}


    class Meta:
        model = UserScore
        fields = ['user_id', 'score_worth', 'timestamp']
