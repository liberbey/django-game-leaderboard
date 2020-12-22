"""
Helper functions for redis sorted sets, here they are called leaderboards.
"""

from api.core.constants import LEADERBOARD, \
    redis_client, COUNTRY_BOARD_PREFIX


def get_leaderboard_name(country_name):
    """
    Returns leaderboard name for country.
    :param country_name: iso code
    :return: name
    """
    return COUNTRY_BOARD_PREFIX + country_name


def create_leaderboard(scores):
    """
    Creates global leaderboard.
    :param scores: mapping that contain keys and scores
    :return: none
    """
    redis_client.zadd(LEADERBOARD, scores)


def get_score(user_id):
    """
    Get score of user from global leaderboard.
    :param user_id: user id
    :return: score, float
    """
    return redis_client.zscore(LEADERBOARD, user_id)


def get_rank(user_id):
    """
    Get global rank of the user.
    :param user_id: user id
    :return: rank, int
    """
    return redis_client.zrevrank(LEADERBOARD, user_id) + 1


def add_user_score(mapping):
    """
    Add user score to global leaderboard.
    :param mapping: userid:score
    :return: none
    """
    redis_client.zadd(LEADERBOARD, mapping)


def add_score_to_country(country_name, mapping):
    """
    Add user score to country leaderboard.
    :param country_name: country
    :param mapping: userid:score
    :return: none
    """
    leaderboard_name = get_leaderboard_name(country_name)
    redis_client.zadd(leaderboard_name, mapping)


def get_all_leaderboard():
    """
    Get global leaderboard.
    :return: leaderboard
    """
    return redis_client.zrange(LEADERBOARD, 0, -1,
                               desc=True, withscores=True)


def get_range_leaderboard(start, end):
    """
    Get users and scores from given range.
    :param start: start index (0-indexed)
    :param end: end index
    :return: part of the leaderboard
    """
    return redis_client.zrevrange(LEADERBOARD, start, end - 1, withscores=True)


def get_range_country_leaderboard(country_name, start, end):
    """
    Get users and scores from given range from specified country leaderboard.
    :param country_name: country
    :param start: start index (0-indexed)
    :param end: end index
    :return: part of the leaderboard
    """
    leaderboard_name = get_leaderboard_name(country_name)
    return redis_client.zrevrange(leaderboard_name, start, end - 1, withscores=True)


def get_country_leaderboard(country_name):
    """
    Get country leaderboard.
    :param country_name: iso code
    :return: country leaderboard
    """
    leaderboard_name = get_leaderboard_name(country_name)
    return redis_client.zrange(leaderboard_name, 0, -1,
                               desc=True, withscores=True)


def increase_user_score(user_id, score):
    """
    Increase the score of the given user by score.
    :param user_id: user id
    :param score: increment
    :return: none
    """
    redis_client.zincrby(LEADERBOARD, score, user_id)


def increase_user_score_country(country_name, user_id, score):
    """
    Increase the score of the user in country table.
    :param country_name: iso code
    :param user_id: userid
    :param score: increment
    :return: none
    """
    leaderboard_name = get_leaderboard_name(country_name)
    redis_client.zincrby(leaderboard_name, score, user_id)


def create_country_leaderboard(country_name, mapping):
    """
    Create country leaderboard.
    :param country_name: iso code
    :param mapping: userid:score
    :return: none
    """
    leaderboard_name = get_leaderboard_name(country_name)
    redis_client.zadd(leaderboard_name, mapping=mapping)
