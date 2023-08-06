import json
import logging
import os
import sys
import redis
from pymongo import MongoClient

from .config import Config, TASK_LOGS_PATH, ROOT_PATH

PROJECT_ID = str(os.environ.get('PROJECT_ID')) or "------"
SPIDER_ID = str(os.environ.get('SPIDER_ID')) or "------"
TASK_ID = str(os.environ.get('TASK_ID')) or "------"

system_config = Config()
redis_client = redis.StrictRedis.from_url(system_config.get('redis_url'))
mongo_client = MongoClient(host=system_config.get('mongo_url'))

task_info = json.loads(redis_client.get('ssti:tasks:' + TASK_ID + ':info') or "{}")
SPIDER_NAME = task_info.get('spider_name') or "------"

LOG_PATH = os.path.join(TASK_LOGS_PATH, TASK_ID + '.log') if TASK_ID != "------" else None
logger = logging.getLogger(PROJECT_ID + ':' + SPIDER_NAME)
