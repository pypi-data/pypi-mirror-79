
white_list = [
    'get', 'set', 'del', 'rpush', 'lpush', 'rpop', 'lpop', 'lrange', 'lindex', 'llen', 'lrem',
    'hget', 'hset', 'hgetall', 'hdel', 'incrby'
]


class NSRedisClient:
    default_url = 'redis://@localhost:6379/6'

    def __init__(self, redis_client, ns):
        self.redis_client = redis_client
        self.ns = ns

    def __getattr__(self, item):

        attr = getattr(self.redis_client, item)

        if attr is None:
            return None

        if not callable(attr):
            return attr

        if item in white_list:
            def op(name, *args, **kwargs):
                return attr(self.ns + ':' + name, *args, **kwargs)

            return op

        return None
