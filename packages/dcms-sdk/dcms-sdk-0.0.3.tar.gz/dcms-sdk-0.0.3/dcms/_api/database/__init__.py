from .redis import NSRedisClient, RedisMQ
from .mongo import *

ns_redis_client = NSRedisClient(redis_client, PROJECT_ID) if NSRedisClient is not None else None
project_mq = RedisMQ(config.PROJECT_ID, redis=config.redis_client)
spider_mq = RedisMQ(config.SPIDER_ID, redis=config.redis_client)
task_mq = RedisMQ(config.TASK_ID, redis=config.redis_client)

__all__ = ["get_database", "get_mongo_collection", "ns_redis_client", "get_system_database", "redis"]
