"""
Helper class for user viewes.
"""


def get_hash_item(data):
    """
    Get hash item from user data.
    :param data: data
    :return: dict
    """
    return {'country': data['country'], 'display_name': data['display_name']}

