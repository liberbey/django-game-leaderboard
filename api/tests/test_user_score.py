"""
UserScore tests.
"""
from rest_framework import status
from rest_framework.test import APITestCase

from api.core.constants import redis_client, LEADERBOARD
from api.core.helpers.redis_leaderboard import get_leaderboard_name


class UserScoreTests(APITestCase):
    """
    Tests for user scores.
    """

    def setUp(self):
        self.display_name = 'l533iberb77ey2323'
        self.user_id = '33536654-77ac-11eb-b378-0242ac130099'
        self.country = 'tt'
        self.score_worth = 15
        url = '/api/user/create/'
        data = '{"display_name": "' + self.display_name + \
               '", "user_id": "' + self.user_id + \
               '", "country": "' + self.country + '"}'
        self.client.generic('POST', url, data,
                            content_type='application/json')

    def test_can_add_score(self):
        """
        Tests create endpoint.
        :return: none
        """
        url = '/api/score/submit/'
        data = '{"score_worth": ' + str(self.score_worth) + \
               ', "user_id": "' + self.user_id + '"}'
        response = self.client.generic('POST', url, data,
                                       content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        redis_client.zrem(LEADERBOARD, self.user_id)
        country_name = get_leaderboard_name(self.country)
        redis_client.zrem(country_name, self.user_id)
        redis_client.delete(self.user_id)
