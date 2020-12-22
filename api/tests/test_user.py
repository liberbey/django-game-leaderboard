"""
Tests for User.
"""
from rest_framework import status
from rest_framework.test import APITestCase

from api.core.constants import redis_client, LEADERBOARD
from api.core.helpers.redis_leaderboard import get_leaderboard_name


class UserTests(APITestCase):
    """
    Tests for user model.
    """

    def setUp(self):
        self.display_name = 'l533iberb77ey2323'
        self.user_id = '33536654-77ac-11eb-b378-0242ac130099'
        self.country = 'tt'

    def test_can_create_user(self):
        """
        Tests create endpoint.
        :return: none
        """
        url = '/api/user/create/'
        data = '{"display_name": "' + self.display_name +\
               '", "user_id": "' + self.user_id +\
               '", "country": "' + self.country + '"}'
        response = self.client.generic('POST', url, data,
                                       content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_read_user(self):
        """
        Tests read endpoint.
        :return: none
        """
        url = '/api/user/create/'
        data = '{"display_name": "' + self.display_name + \
               '", "user_id": "' + self.user_id + \
               '", "country": "' + self.country + '"}'
        self.client.generic('POST', url, data,
                            content_type='application/json')
        url = '/api/user/profile/' + self.user_id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        redis_client.zrem(LEADERBOARD, self.user_id)
        country_name = get_leaderboard_name(self.country)
        redis_client.zrem(country_name, self.user_id)
        redis_client.delete(self.user_id)
