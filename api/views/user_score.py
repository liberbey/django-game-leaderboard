"""
Classes for user-score views.
"""
from datetime import datetime

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.core.helpers import redis_hash, redis_leaderboard
from api.serializers.user_score import UserScoreSerializer


class UserScoreView(APIView):
    """
    User Score view.
    """
    permission_classes = []
    authentication_classes = []
    renderer_classes = [JSONRenderer]

    def post(self, request, format=None):
        """
        Creates a userScore objects, add it to redis leaderboards.
        :param request: request
        :param format: format
        :return: json response
        :return: json response
        """
        serializer = UserScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_id = str(serializer.data["user_id"])
            user_info = redis_hash.get_all(user_id)
            redis_leaderboard.increase_user_score(user_id, serializer.data["score_worth"])
            redis_leaderboard.increase_user_score_country(
                user_info['country'], user_id, serializer.data["score_worth"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
