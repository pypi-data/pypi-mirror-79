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


class RedisMQ:
    _msg_addr = 'rmq:default'
    redis_url = 'redis://@localhost:6379/6'

    def __init__(self, message_addr=None, redis=None, redis_url=None):
        pass

    def send(self, msg_content, to_addr='default'):
        """"""""

    def reply(self, msg_content, to_addr='default', reply_id=None):
        """"""

    def send_stream(self, data, to_addr='default', reply_id=None):
        """"""

    def read_stream(self, stream, timeout=6):
        """"""

    def read_stream_raw(self, stream, timeout=6):
        """"""

    def wait(self, timeout=None):
        """"""

    def wait_to_read_raw(self, timeout=None, reply_id=None):
        """"""

    def wait_to_read(self, timeout=None, reply_id=None):
        """"""

    def wait_reply(self, reply_id, timeout=None):
        """"""

    def clear_msg(self):
        """"""

    def get(self):
        """"""
