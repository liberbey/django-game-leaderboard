"""
Helpers for leaderboard viewes.
"""

from api.core.helpers import redis_hash


def get_response_data(data, start=0):
    """
    Returns response data from fiven sorted set data.
    :param data: data from sorted set
    :param start: start index
    :return: response data
    """
    response_data = []
    for i, element in enumerate(data):
        user_id = element[0]
        json_obj = redis_hash.get_all(user_id)
        json_obj['rank'] = start + i + 1
        json_obj['points'] = int(element[1])
        response_data.append(json_obj)
    return response_data
