from api import system_config
from api.database import get_database


class ProxyPool:

    def __init__(self, zone='all'):
        self.proxies_collection_name = system_config.get('proxies_collection_name')

        self.proxies_collection = get_database().get_collection(self.proxies_collection_name)

        self._proxies_cache = {}

    def get_proxies(self, limit=100, zone='all'):
        condition = {}
        if zone != 'all':
            condition['zone'] = zone
        return self.proxies_collection.find(condition, limit=limit, sort=[('score', -1)])

    def get_proxies_random(self, limit=100, zone='all'):
        condition = {}
        if zone != 'all':
            condition['zone'] = zone
        return self.proxies_collection.aggregate(
            [
                {'$match': condition or {}},
                {'$sample': {'size': limit}}
            ])

    def get_one_proxy(self, zone='all'):
        zone_proxies = self._proxies_cache.get(zone)
        if not isinstance(zone_proxies, list) or len(zone_proxies) < 1:
            zone_proxies = [item for item in self.get_proxies_random(zone=zone)]
            self._proxies_cache[zone] = zone_proxies

        return zone_proxies.pop(-1) if len(zone_proxies) > 0 else None
