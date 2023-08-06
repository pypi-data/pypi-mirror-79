from .redis import NSRedisClient
from .mongo import *

ns_redis_client = NSRedisClient(redis_client, PROJECT_ID) if NSRedisClient is not None else None
__all__ = ["get_database", "get_mongo_collection", "ns_redis_client", "get_system_database", "redis"]
