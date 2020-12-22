"""
View classes for country leaderboard requests.
"""

from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from api.core.helpers import redis_hash, redis_leaderboard
from api.core.helpers.leaderboard_helper import get_response_data
from api.core.helpers.redis_hash import get_all
from api.core.helpers.redis_leaderboard import get_range_country_leaderboard,\
    get_country_leaderboard


class LeaderboardCountryListView(APIView):
    """
    Class for listing whole country leaderboard.
    """
    permission_classes = []
    authentication_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request, iso_code):
        """
        Get response. Get all data from country leaderboard,
        then get user info from hash and return.
        :param request: request
        :param iso_code: country code
        :return: response as json
        """
        data = redis_leaderboard.get_country_leaderboard(iso_code)
        response_data = []
        for element in data:
            user_id = element[0]
            json_obj = redis_hash.get_all(user_id)
            json_obj['rank'] = redis_leaderboard.get_rank(user_id)
            json_obj['points'] = int(element[1])
            response_data.append(json_obj)
        return Response(response_data)


class LeaderboardCountryRangeView(APIView):
    """
    Class for listing country leaderboard with a given range.
    """
    permission_classes = []
    authentication_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request, iso_code):
        """
        List leaderboard with a start and offset.
        :param request: request
        :param iso_code: country code
        :return: json response
        """
        if 'start' in request.query_params and 'offset' in request.query_params:
            start = int(request.query_params['start'])
            offset = int(request.query_params['offset'])
            data = get_range_country_leaderboard(iso_code, start, start+offset)
            response_data = get_response_data(data, start=start)
            return Response(response_data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LeaderboardCountryStreamView(APIView):
    """
    Stream listing whole global leaderboard.
    """
    permission_classes = []
    authentication_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request, iso_code):
        """
        Creates a response stream consisting of chunks.
        :param request: request
        :return: streaming http response
        """
        data = get_country_leaderboard(iso_code)
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
