import json
import os
import pickle

# from .database import get_system_database
from .init import PROJECT_ID, redis_client
from .config import CACHE_DIR
from .config import redis_keys


class DataStore(object):

    def __init__(self, store_path):

        self.data = {}

        self.store_path = store_path

        self.dirname = os.path.dirname(store_path)

        if os.path.exists(self.dirname):
            if os.path.isfile(store_path):
                try:
                    f = open(store_path, 'r')
                    text = f.read()
                    self.data = json.loads(text)
                except Exception as e:
                    self.data = {}
            elif os.path.isdir(store_path):
                pass
        else:
            self.data = {}
            os.makedirs(self.dirname)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def save(self):

        with open(self.store_path, 'w') as f:
            f.write(json.dumps(self.data))


class DiskStore(DataStore):
    pass


class RedisStore(object):

    def __init__(self, store_name, project_id=None):
        self.redis_client = redis_client
        self.name = store_name
        self.redis_key = redis_keys.REDIS_STORE_BASE.format((project_id or PROJECT_ID) + ":" + store_name)

    def get(self, key):
        result = self.redis_client.hget(self.redis_key, key)
        if result:
            return pickle.loads(result)
        return result

    def set(self, key, value):
        return self.redis_client.hset(self.redis_key, key, pickle.dumps(value))

    def get_all(self):
        data = self.redis_client.hgetall(self.redis_key) or {}
        result = {}
        for key in data:
            try:
                result[key] = pickle.loads(data[key])
            except Exception as e:
                result[key] = data[key]
        return result


def get_cache_dir():
    cache_dir = os.path.join(CACHE_DIR, PROJECT_ID)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    return cache_dir
