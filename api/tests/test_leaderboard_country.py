"""
Tests country leaderboard.
"""
from rest_framework import status
from rest_framework.test import APITestCase

from api.core.constants import redis_client, LEADERBOARD
from api.core.helpers.redis_leaderboard import get_leaderboard_name


class CountryLeaderboardTests(APITestCase):
    """
    Tests for country leaderboard.
    """
    def setUp(self):
        self.display_name = 'l533iberb77ey2323'
        self.user_id = '33536654-77ac-11eb-b378-0242ac130099'
        self.country = 'aa'
        self.score_worth = 15
        url = '/api/user/create/'
        data = '{"display_name": "' + self.display_name + \
               '", "user_id": "' + self.user_id + \
               '", "country": "' + self.country + '"}'
        self.client.generic('POST', url, data,
                            content_type='application/json')

    def test_can_read_country_leaderboard(self):
        """
        Tests read endpoint.
        :return: none
        """
        url = '/api/leaderboard/' + self.country + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_country_stream(self):
        """
        Tests stream endpoint.
        :return: none
        """
        url = '/api/leaderboard/country/' + self.country + '/stream/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        redis_client.zrem(LEADERBOARD, self.user_id)
        country_name = get_leaderboard_name(self.country)
        redis_client.zrem(country_name, self.user_id)
        redis_client.delete(self.user_id)
