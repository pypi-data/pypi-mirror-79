import redis
from hwhpykit.cache.reids.RedisStringManager import RedisStringManager
from hwhpykit.cache.reids.RedisHashManager import RedisHashManager
from hwhpykit.cache.reids.RedisListManager import RedisListManager
from hwhpykit.cache.reids.RedisSetManager import RedisSetManager
from hwhpykit.cache.reids.RedisZSetManager import RedisZSetManager


class RedisManager(object):
    __redis = None
    __pool = None
    __tag = ""

    string = RedisStringManager
    hash = RedisHashManager
    set = RedisSetManager
    zset = RedisZSetManager
    list = RedisListManager

    @classmethod
    def config(cls, host='127.0.0.1', port=6379, db=0, password=''):
        cls.pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
        cls.redis = redis.Redis(connection_pool=cls.pool)
        cls.set = RedisSetManager.config(cls.redis)
        cls.hash = RedisHashManager.config(cls.redis)
        cls.zset = RedisZSetManager.config(cls.redis)
        cls.string = RedisStringManager.config(cls.redis)
        cls.list = RedisListManager.config(cls.redis)
        return cls

    @classmethod
    def check_connect(cls):
        if cls.redis is None or cls.pool is None:
            raise Exception("redis config error")


