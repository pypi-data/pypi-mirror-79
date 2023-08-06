import json

TASK_LOGS_PATH = ''
ROOT_PATH = ''
CACHE_DIR = ''


class Config:
    _file_path = ''

    def __init__(self):
        self._setting = {}
        self.init()

    def init(self):
        self._setting = {}

    def get(self, key):
        return self._setting.get(key)

    @classmethod
    def get_from_json(cls, key):
        result = None
        with open(cls._file_path) as f:
            result = f.read()
            # _setting = json.loads(text)
            # for key in _setting:
            #     _setting[key] = json.dumps(_setting[key])
        result = json.loads(result)
        return result.get(key)

    def set(self, key, value):
        self._setting[key] = value
        self.save()

    def save(self):
        pass

    def set_all(self, setting):
        self._setting.update(setting)
        self.save()

        return True

    def get_all(self):
        return self._setting

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)


class RedisKeys:
    REDIS_STORE_BASE = ''


redis_keys = RedisKeys()
