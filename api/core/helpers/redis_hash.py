"""
Helper functions for redis hashes.
"""

from api.core.constants import redis_client


def create_hash(name, mapping):
    """
    Creates a redis hash in memory.
    :param name: name of the hash
    :param mapping: fields to store
    :return: none
    """
    redis_client.hset(name, mapping=mapping)


def get_all(hash_name):
    """
    Get all fields in a hash.
    :param hash_name: name of the hash
    :return: field dict
    """
    return redis_client.hgetall(hash_name)
