import os

if os.environ.get('IN_CRAWL_PROCESS'):
    from api.ext import *

else:
    from .._api.ext import *

