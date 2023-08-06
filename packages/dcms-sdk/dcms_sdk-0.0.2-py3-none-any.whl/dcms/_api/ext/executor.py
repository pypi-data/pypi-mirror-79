import json
import os

import scrapy
import yaml
from scrapy import Spider

from api import task_info
from config import PROJECTS_PATH


class Executor(Spider):

    def __init__(self):
        super(Executor, self).__init__()
        _config_path = task_info.get('file_path')
        _project_id = task_info.get('project_id')
        project_path = os.path.join(PROJECTS_PATH, _project_id)
        config_path = os.path.join(project_path, _config_path)
        self.config = yaml.load(open(config_path).read())
        # self.config = json.loads(task_info.get('config')) or {}
        self.init(self.config)

    def init(self, config):
        pass
