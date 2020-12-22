"""
Classes for user Views.
"""
import uuid

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.core.helpers import redis_hash, redis_leaderboard
from api.core.helpers.user_helper import get_hash_item
from api.models.user_score import UserScore
from api.serializers.user import UserSerializer


class UserGetView(APIView):
    """
    Class for user info.
    """
    permission_classes = []
    authentication_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request, user_id):
        """
        Get user details.
        :param request: request
        :param user_id: user_id
        :return: json response
        """
        data = redis_hash.get_all(user_id)
        data['user_id'] = user_id
        data['points'] = int(redis_leaderboard.get_score(user_id))
        data['rank'] = redis_leaderboard.get_rank(user_id)
        return Response(data)


class UserCreateView(APIView):
    """
    Create view for users.
    """
    permission_classes = []
    authentication_classes = []
    renderer_classes = [JSONRenderer]

    def post(self, request, format=None):
        """
        Create user, add it to both db and redis leaderboards/hash.
        :param request: request
        :param format: format
        :return:
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()
            user_info = get_hash_item(serializer.data)
            redis_hash.create_hash(serializer.data['user_id'], user_info)
            points = 0
            if 'points' in request.data:
                points = request.data['points']
            user_score = UserScore.objects.create(user_id=user_obj,
                                                  score_worth=points)
            user_score.save()
            score_mapping = {str(serializer.data['user_id']): points}
            redis_leaderboard.add_user_score(score_mapping)
            redis_leaderboard.add_score_to_country(user_info['country'], score_mapping)
            data = serializer.data
            data['rank'] = redis_leaderboard.get_rank(data['user_id'])
            data['points'] = points
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
