"""
API constants.
"""
import logging
import redis

logger = logging.getLogger('django')
redis_client = redis.StrictRedis(
    host='redis-14556.c12.us-east-1-4.ec2.cloud.redislabs.com', port=14556, db=0,
    charset="utf-8", password='112358', decode_responses=True)

LEADERBOARD = 'leaderboard'
USER_MAP = 'user_map'
USERS_INIT_SQL = "select * from users"
COUNTRY_BOARD_PREFIX = 'leaderboard_'
LEADERBOARD_INIT_SQL = "select users.country, users.user_id, tmp.tot_score from users left join " \
                       "(select user_id, sum(score_worth) as tot_score from " \
                       "user_score group by user_id order by tot_score desc) as tmp" \
                       " on users.user_id = tmp.user_id"
