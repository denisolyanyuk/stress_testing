import uuid

import redis
from django.conf import settings

REDIS_HOST = 'redis_stres_testing'
REDIS_PORT = 6379
REDIS_DB = 0

class RedisClient(object):

    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB)

    @property
    def conn(self):
        if not hasattr(self, '_conn'):
            self._get_connection()
        return self._conn

    def _get_connection(self):
        self._conn = redis.Redis(connection_pool=self.pool)


redis_connection = RedisClient().conn