"""
API app.
"""

from django.apps import AppConfig
from django.db import connection

from api.core.helpers import redis_hash, redis_leaderboard
from api.core.constants import USERS_INIT_SQL, LEADERBOARD_INIT_SQL, logger
import orjson as json
import uuid


def get_users_dict(cursor):
    """
    Return a dict such that id:json(fields).
    :param cursor: db response
    :return: dict
    """
    element_dict = {}
    columns = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        element_dict[get_uuid_str(row[1])] = json.dumps({columns[0]: row[0], columns[3]: row[3]})
    return element_dict


def get_users_list(cursor):
    """
    Return a dict such that id:json(fields)
    :param cursor: db response
    :return: users list for hash
    """
    element_list = []
    columns = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        element_list.append((get_uuid_str(row[1]), {columns[0]: row[0], columns[3]: row[3]}))
    return element_list


def get_scores_dict(cursor):
    """
    Return a dict such that id:score and country:users
    :param cursor: db response
    :return: two dicts
    """
    element_dict = {}
    country_dicts = {}
    for row in cursor.fetchall():
        country = row[0]
        user_id = row[1]
        score = row[2]
        element_dict[get_uuid_str(user_id)] = score
        if country in country_dicts:
            country_dicts[country][get_uuid_str(user_id)] = score
        else:
            country_dicts[country] = {}
            country_dicts[country][get_uuid_str(user_id)] = score
    return element_dict, country_dicts


def get_uuid_str(id_str):
    """
    Helper function for uuid-string conversion.
    :param id_str: id_str
    :return: uuid as str
    """
    return str(uuid.UUID(id_str))


class ApiConfig(AppConfig):
    """
    ApiConfig.
    """
    name = 'api'

    def ready(self):
        """
        This function is called at initilization.
        :return: none
        """
        import sys
        if 'runserver' in sys.argv:
            logger.info("API app is ready to start.")
            # First, create redis sorted sets as leaderboards.
            with connection.cursor() as cursor:
                logger.info("Running SQL query for leaderboards initialization: " + LEADERBOARD_INIT_SQL)
                cursor.execute(LEADERBOARD_INIT_SQL)
                scores, country_dicts = get_scores_dict(cursor)
            if len(scores) > 0:
                logger.info("Creating redis sorted sets as leaderboards.")
                redis_leaderboard.create_leaderboard(scores)
                for country in country_dicts:
                    redis_leaderboard.create_country_leaderboard(country, country_dicts[country])

            # Then, create redis hash for user infos.
            with connection.cursor() as cursor:
                logger.info("Running SQL query for hash initialization: " + USERS_INIT_SQL)
                cursor.execute(USERS_INIT_SQL)
                user_list = get_users_list(cursor)
            if len(user_list) > 0:
                logger.info("Creating user hashes.")
                for user in user_list:
                    redis_hash.create_hash(user[0], user[1])

