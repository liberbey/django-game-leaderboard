"""
Tests for global leaderboard.
"""
from rest_framework import status
from rest_framework.test import APITestCase


class GlobalLeaderboardTests(APITestCase):
    """
    Tests for global leaderboard.
    """

    def test_can_read_global_leaderboard(self):
        """
        Tests read endpoint.
        :return: none
        """
        url = '/api/leaderboard/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stream_response(self):
        """
        Tests stream endpoint.
        :return: none
        """
        url = '/api/leaderboard/stream/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
