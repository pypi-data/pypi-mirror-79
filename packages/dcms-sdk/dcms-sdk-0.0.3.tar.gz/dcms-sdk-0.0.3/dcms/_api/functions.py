from .data import *


def update_data_count(item, saved=False):
    return item


def inc_data_count_record(count):
    return 1


def inc_crawled_count(count=1):
    return 1


def inc_saved_count(count=1):
    return 1


def save_item(item):
    return item


def replace_item(_id, item):
    return _id


def save_or_replace_item(item, _id=None):
    return item


def record_item(item):
    return item


def record_item_list(item_list):
    return 0


def record_task_status(status):
    pass


def get_settings():
    return {}
