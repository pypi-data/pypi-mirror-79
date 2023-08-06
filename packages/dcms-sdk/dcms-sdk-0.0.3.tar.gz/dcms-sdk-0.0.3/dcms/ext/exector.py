import os

if os.environ.get('IN_CRAWL_PROCESS'):
    from api.ext.exector import *

else:
    from .._api.ext.executor import *

