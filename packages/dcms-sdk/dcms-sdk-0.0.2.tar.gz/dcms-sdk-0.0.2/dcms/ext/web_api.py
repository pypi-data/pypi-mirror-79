import os

if os.environ.get('IN_CRAWL_PROCESS'):
    from api.ext.web_api import *

else:
    from .._api.ext.web_api import *
