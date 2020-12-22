"""
View classes for global leaderboard requests.
"""
from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.core.helpers.leaderboard_helper import get_response_data
from api.core.helpers.redis_hash import get_all
from api.core.helpers.redis_leaderboard import get_range_leaderboard, get_all_leaderboard


class LeaderboardListView(APIView):
    """
    Class for listing whole global leaderboard.
    """
    permission_classes = []
    authentication_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request):
        """
        Get all entries in the leaderboard.
        :param request: request
        :return: json response
        """
        data = get_all_leaderboard()
        response_data = get_response_data(data)
        return Response(response_data)


class LeaderboardRangeView(APIView):
    """
    Class for listing global leaderboard with a range.
    """
    permission_classes = []
    authentication_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request):
        """
        Gets elements in leaderboard between start and start+offset.
        :param request: request
        :return: json response
        """
        if 'start' in request.query_params and 'offset' in request.query_params:
            start = int(request.query_params['start'])
            offset = int(request.query_params['offset'])
            data = get_range_leaderboard(start, start+offset)
            response_data = get_response_data(data, start=start)
            return Response(response_data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LeaderboardStreamView(APIView):
    """
    Stream listing for country leaderboard.
    """
    permission_classes = []
    authentication_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request):
        """
        Creates a response stream consisting of chunks.
        :param request: request
        :return: streaming http response
        """
        data = get_all_leaderboard()
        return StreamingHttpResponse(self.stream_response_generator(data))

    def stream_response_generator(self, data):
        """
        Generates stream response.
        :return: parts of the response
        """
        yield '['
        for i, element in enumerate(data):
            if i != 0:
                yield ','
            user_id = element[0]
            json_obj = get_all(user_id)
            json_obj['rank'] = i + 1
            json_obj['points'] = int(element[1])
            yield json_obj
        yield ']'
